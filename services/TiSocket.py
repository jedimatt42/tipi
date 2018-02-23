import logging
import errno
import socket
import fcntl

# Represent socket access from Raw extensions. This is registered as 0x22 in RawExtensions.py
#  usage: send a message starting with 0x22 as the first byte. 
#   second byte should be socket handle number to use
#   third byte is command for handle: 0x01 open, 0x02 close, 0x03 write, 0x04 read
#   
#   For 0x01 open / follow with string in the form of "hostname:port" 
#     Tipi will return a message of 255 if connected or 0 if failed to connect.
#   For 0x02 close / no parameters
#     Tipi will return 255
#   For 0x03 write / follow with bytes to write to socket
#     Tipi will return after bytes are written with 255 or 0 if failed to write.
#   For 0x04 read / follow with max size to read as int (two bytes, [msb,lsb])
#     Tipi will return message of available socket data no greater than max size.
#
#   socket handle numbers are a single byte 0-255
#

logger = logging.getLogger(__name__)

GOOD = bytearray([255])
BAD = bytearray([0])

class TiSocket(object):

    def __init__(self, tipi_io):
        self.tipi_io = tipi_io
        self.handles = { }
        self.commands = {
                0x01 : self.handleOpen,
                0x02 : self.handleClose,
                0x03 : self.handleWrite,
                0x04 : self.handleRead
                }

    def handle(self, bytes):
        self.tipi_io.send(self.processRequest(bytes))
        return True

    def processRequest(self, bytes):
        try:
            command = bytes[2]
            commandHandler = self.commands.get(command, self.defaultHandler)
            return commandHandler(bytes)
        except IOError as e:
            return BAD

    def defaultHandler(self, bytes):
        logger.error("unknown command: %d", bytes[2])
        return BAD

    # bytes: 0x22, handleId, open-cmd, <hostname:port>
    def handleOpen(self, bytes):
        handleId = bytes[1]
        existing = self.handles.get(handleId, None)
        # close the socket if we already had one for this handle.
        if not existing is None:
            self.handles.remove(handleId)
            self.safeClose(existing)
            existing = None
        # need to get the target host and port
        params = str(bytes[3:]).split(':')
        hostname = params[0]
        port = params[1]
        server = (hostname, port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.handles[handleId] = sock
        try:
            sock.connect(server)
            fcntl.fcntl(sock, fcntl.F_SETFL, os.O_NONBLOCK)
            return GOOD
        except Exception as e:
            self.safeClose(sock)
            return BAD

    # bytes: 0x22, handleId, close-cmd
    def handleClose(self, bytes):
        handleId = bytes[1]
        existing = self.handles.get(handleId, None)
        if not existing is None:
            self.handles.remove(handleId)
            self.safeClose(existing)
        return GOOD

    # bytes: 0x22, handleId, write-cmd, <bytes to write>
    def handleWrite(self, bytes):
        handleId = bytes[1]
        existing = self.handles.get(handleId, None)
        if existing is None:
            return BAD
        try:
            existing.sendall(bytes[3:])
            return GOOD
        except Exception as e:
            self.handles.remove(handleId)
            self.safeClose(existing)
            return BAD

    # bytes: 0x22, handleId, read-cmd, MSB, LSB
    def handleRead(self, bytes):
        handleId = bytes[1]
        existing = self.handles.get(handleId, None)
        if existing is None:
            return BAD
        limit = (bytes[3] << 8) + bytes[4]
        data = bytearray(existing.recv(limit))
        return data

    def safeClose(self, socket):
        try:
            socket.close()
        except Exception as e:
            pass

