import logging

from Pab import (
    opcode, recordLength,
    EOPATTR, EFILERR, SUCCESS,
    OPEN, CLOSE, READ, WRITE,
)
from TiSocket import ACCEPT_ERR, BAD, TiSocket

logger = logging.getLogger(__name__)


class TcpFile(object):

    @staticmethod
    def filename():
        # open file in "append" mode, such as:
        #   PI.TCP=<hostname/ipv4-addr>:<port>
        # for server socket:
        #   PI.TCP=<interface>:<port>.BIND
        #      input handle
        #   PI.TCP=<interface>:<port>.<handle>
        return "TCP="

    def __init__(self, tipi_io):
        self.tipi_io = tipi_io
        self.handles = {}
        self.tisockets = TiSocket(tipi_io)

    def handle(self, pab, devname):
        op = opcode(pab)
        if op == OPEN:
            self.open(pab, devname)
        elif op == CLOSE:
            self.close(pab, devname)
        elif op == READ:
            self.read(pab, devname)
        elif op == WRITE:
            self.write(pab, devname)
        else:
            self.tipi_io.send([EOPATTR])

    def close(self, pab, devname):
        logger.info("close devname: %s", devname)
        try:
            if devname in self.handles.keys():
                self.closeConnection(devname)
            elif devname.endswith('BIND'):
                self.unbind(devname)
        except Exception as e:
            logger.error(e, exc_info=True)
        self.tipi_io.send([SUCCESS])

    def closeConnection(self, devname):
        msg = bytearray(3)
        msg[0] = 0x22
        msg[1] = self.handles[devname]
        msg[2] = 0x02
        self.tisockets.processRequest(msg)
        del(self.handles[devname])

    def unbind(self, devname):
        msg = bytearray(3)
        msg[0] = 0x22
        msg[1] = 0x00
        msg[2] = 0x06
        self.tisockets.processRequest(msg)

    def open(self, pab, devname):
        logger.debug("open devname: %s", devname)
        try:
            (host, port, binding) = self.parseDev(devname)
            if not binding:
                self.connectClient(devname, host, port)
            elif binding == "BIND":
                self.bindServer(host, port)
            elif binding:
                self.openIncoming(devname, binding)
        except Exception as e:
            logger.error(e, exc_info=True)
            self.tipi_io.send([EFILERR])
            return

        recLen = recordLength(pab)
        if recLen == 0:
            recLen = 80
        self.tipi_io.send([SUCCESS])
        self.tipi_io.send([recLen])
        return

    def connectClient(self, devname, host, port):
        handleId = self.tisockets.allocateHandleId()
        address = host + ':' + port
        msg = bytearray(len(address) + 3)
        msg[0] = 0x22
        msg[1] = handleId
        msg[2] = 0x01
        msg[3:] = bytearray(address, 'ascii')
        res = self.tisockets.processRequest(msg)
        if res == BAD:
            raise Exception("error opening socket")
        self.handles[devname] = handleId

    def bindServer(self, host, port):
        iface_addr = host + ':' + port
        logger.info(f'BIND, interface address: {iface_addr}')
        msg = bytearray(len(iface_addr) + 3)
        msg[0] = 0x22
        # from DSR level 3 io, we'll only do one listening port
        # it's an old computer.
        msg[1] = 0x00
        msg[2] = 0x05
        msg[3:] = bytearray(iface_addr, 'ascii')
        res = self.tisockets.processRequest(msg)
        if res == BAD:
            raise Exception("error binding port")

    def openIncoming(self, devname, binding):
        # TODO: check that binding matches handle
        self.handles[devname] = int(binding)

    def read(self, pab, devname):
        logger.info("read devname: %s", devname)

        if devname.endswith('BIND'):
            self.accept(devname)
        else:
            self.readConnection(pab, devname)
        return

    def accept(self, devname):
        logger.info("accepting from devname: %s", devname)
        msg = bytearray(3)
        msg[0] = 0x22
        msg[1] = 0x00
        msg[2] = 0x07
        res = self.tisockets.processRequest(msg)
        if res == ACCEPT_ERR:
            logger.error("accept error, devname: %s", devname)
            self.tipi_io.send([EFILERR])
        else:
            # If there was no error, but no pending connect this just passes
            # the zero back through the read operation.
            logger.info("accept success, handle: %d, devname: %s", res[0], devname)
            self.tipi_io.send([SUCCESS])
            self.tipi_io.send(bytearray(str(int(res[0])), 'ascii'))

    def readConnection(self, pab, devname):
        handleId = self.handles[devname]
        msg = bytearray(5)
        buf_len = recordLength(pab)
        msg[0] = 0x22
        msg[1] = handleId
        msg[2] = 0x04
        msg[3] = (buf_len & 0xFF00) >> 8
        msg[4] = buf_len & 0xFF
        res = self.tisockets.processRequest(msg)
        if res == BAD:
            raise Exception('error reading socket')
        self.tipi_io.send([SUCCESS])
        self.tipi_io.send(res)

    def write(self, pab, devname):
        logger.info("write devname: %s", devname)
        if devname.endswith('BIND'):
            raise Exception('not supported')

        handleId = self.handles[devname]
        self.tipi_io.send([SUCCESS])
        data = self.tipi_io.receive()

        msg = bytearray(len(data) + 3)
        msg[0] = 0x22
        msg[1] = handleId
        msg[2] = 0x03
        msg[3:] = data
        res = self.tisockets.processRequest(msg)
        if res == BAD:
            raise Exception('failed to write to socket')
        self.tipi_io.send([SUCCESS])

    def parseDev(self, devname):
        parts = devname.split("=")[1].split(":")
        host_iface = parts[0]
        if '.' in parts[1]:
            parts = parts[1].split(".")
            port = parts[0]
            handle = parts[1]
        else:
            port = parts[1]
            handle = ""
        logger.info('tcp devname: %s, %s, %s', host_iface, port, handle)
        return (host_iface, port, handle)
