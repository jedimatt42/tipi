import struct
import fcntl
import os
import logging

logger = logging.getLogger(__name__)

class Mouse(object):

    def __init__(self, tipi_io):
        self.tipi_io = tipi_io
        self.file = open("/dev/input/mice", "rb")
        fd = self.file.fileno()
        flag = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, flag | os.O_NONBLOCK)
        self.button = 0

    def getMouseEvent(self):
        try:
            buf = self.file.read(3)
            self.button = ord(buf[0])
            x, y = struct.unpack("bb", buf[1:]);
            logger.debug("x %d, y %d, b %d", x, y, self.button)
            return bytearray(struct.pack('bbb', x, -1 * y, self.button))
        except IOError as e:
            return bytearray([0, 0, self.button])

    def handle(self, bytes):
        self.tipi_io.send(self.getMouseEvent())
        return True
