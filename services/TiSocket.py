import os
import logging
import errno
import socket
import fcntl
from Oled import oled

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
        params = str(bytes[3:]).split(':')
        hostname = params[0]
        port = int(params[1])
        logger.info("open socket(%d) %s:%d", handleId, hostname, port)

        existing = self.handles.get(handleId, None)
        # close the socket if we already had one for this handle.
        if not existing is None:
            del(self.handles[handleId])
            self.safeClose(existing)
            existing = None
            logger.debug("closed leftover socket: %d", handleId)
        # need to get the target host and port
        server = (hostname, port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.handles[handleId] = sock
        try:
            sock.connect(server)
            fcntl.fcntl(sock, fcntl.F_SETFL, os.O_NONBLOCK)
            logger.info("connected")
            oled.info("Socket %d/Connected", handleId)
            return GOOD
        except Exception as e:
            logger.info("failed to connect socket: %d", handleId, exc_info=True)
            self.safeClose(sock)
            return BAD

    # bytes: 0x22, handleId, close-cmd
    def handleClose(self, bytes):
        handleId = bytes[1]
        existing = self.handles.get(handleId, None)
        if not existing is None:
            del(self.handles[handleId])
            self.safeClose(existing)
            logger.info("closed socket: %d", handleId)
            oled.info("Socket %d/Closed", handleId)
        return GOOD

    # bytes: 0x22, handleId, write-cmd, <bytes to write>
    def handleWrite(self, bytes):
        handleId = bytes[1]
        existing = self.handles.get(handleId, None)
        if existing is None:
            return BAD
        try:
            existing.sendall(bytes[3:])
            logger.debug("wrote %d bytes to socket: %d", len(bytes[3:]), handleId)
            oled.info("Socket %d/Wrote %d bytes", handleId, len(bytes[3:]))
            return GOOD
        except Exception as e:
            del(self.handles[handleId])
            self.safeClose(existing)
            logger.info("failed to write to socket: %d", handleId)
            return BAD

    # bytes: 0x22, handleId, read-cmd, MSB, LSB
    def handleRead(self, bytes):
        try:
            handleId = bytes[1]
            logger.debug("read socket: %d", handleId)
            existing = self.handles.get(handleId, None)
            if existing is None:
                logger.info("socket not open: %d", handleId)
                return bytearray(0)
            limit = (bytes[3] << 8) + bytes[4]
            data = bytearray(existing.recv(limit))
            logger.debug("read %d bytes from %d", len(data), handleId)
            oled.info("Socket %d/Read %d bytes", handleId, len(data))
            return data
        except socket.error as e:
            err = e.args[0]
            if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                logger.debug("no data ready: %d", handleId)
                return bytearray(0)
            else:
                logger.error(e, exc_info=True)
        except Exception as e:
            logger.error(e, exc_info=True)
        return BAD


    def safeClose(self, socket):
        try:
            socket.close()
        except Exception as e:
            pass

