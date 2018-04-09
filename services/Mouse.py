import struct
import fcntl
import os
from TipiConfig import TipiConfig


tipi_config = TipiConfig.instance()

class Mouse(object):

    def __init__(self, tipi_io):
        self.tipi_io = tipi_io
        self.file = open("/dev/input/mice", "rb")
        fd = self.file.fileno()
        flag = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, flag | os.O_NONBLOCK)
        self.scale = float(tipi_config.get("MOUSE_SCALE", "60")) / 100.0
        self.sf = 5

    def getMouseEvent(self):
        try:
            buf = self.file.read(3)
            button = ord(buf[0])
            x, y = struct.unpack("bb", buf[1:]);
            if abs(x) > self.sf:
                if x > 0:
                    x = max(self.sf,int(x * self.scale))
                else:
                    x = min(-1 * self.sf,int(x * self.scale))
            if abs(y) > self.sf:
                if y > 0:
                    y = max(self.sf,int(y * self.scale))
                else:
                    y = min(-1 * self.sf,int(y * self.scale))
            return bytearray(struct.pack('bbb', x, -1 * y, button))
        except IOError as e:
            return bytearray([0, 0, 0])

    def handle(self, bytes):
        self.tipi_io.send(self.getMouseEvent())
        return True
