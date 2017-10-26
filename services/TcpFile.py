import os
import socket
import errno
import fcntl
import logging

from Pab import *

logger = logging.getLogger(__name__)


class TcpFile(object):

    @staticmethod
    def filename():
        # open file in "append" mode, such as:
        #   TIPI.TCP=<hostname/ipv4-addr>:<port>
        return "TIPI.TCP="

    def __init__(self, tipi_io):
        self.tipi_io = tipi_io
        self.sock = {}

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
        logger.debug("close devname: %s", devname)
        self.tipi_io.send([SUCCESS])
        try:
            if self.sock[devname]:
                self.sock[devname].close()
                del(self.sock[devname])
        except BaseException:
            pass

    def open(self, pab, devname):
        logger.debug("open devname: %s", devname)
        try:
            server = self.parseDev(devname)
            logger.debug("host %s, port %s", server[0], server[1])
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(server)
            fcntl.fcntl(sock, fcntl.F_SETFL, os.O_NONBLOCK)
            self.sock[devname] = sock
        except socket.error as e:
            logger.error(e, exc_info=True)
            self.tipi_io.send([EFILERR])
            return

        recLen = recordLength(pab)
        if recLen == 0:
            recLen = 80
        self.tipi_io.send([SUCCESS])
        self.tipi_io.send([recLen])
        return

    def read(self, pab, devname):
        logger.debug("read devname: %s", devname)
        try:
            sock = self.sock[devname]
            fdata = bytearray(sock.recv(recordLength(pab)))
            logger.debug("read from socket: %s", str(fdata))
            self.tipi_io.send([SUCCESS])
            self.tipi_io.send(fdata)
            return
        except socket.error as e:
            err = e.args[0]
            if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                fdata = bytearray("")
                self.tipi_io.send([SUCCESS])
                self.tipi_io.send(fdata)
                return
        self.tipi_io.send([EFILERR])
        return

    def write(self, pab, devname):
        logger.debug("write devname: %s", devname)
        try:
            sock = self.sock[devname]
            self.tipi_io.send([SUCCESS])
            msg = self.tipi_io.receive()
            sock.sendall(msg)
        except socket.error as e:
            self.sock[devname].close()
            del(self.sock[devname])

    def parseDev(self, devname):
        parts = str(devname).split("=")[1].split(":")
        return (parts[0], int(parts[1]))
