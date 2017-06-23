import struct
import fcntl
import os

# Issues: reading from file is blocking IO. 
# Can't be blocking the TI-99/4A like that. 

class Mouse(object):

    def __init__(self, tipi_io):
        self.tipi_io = tipi_io
        self.file = open( "/dev/input/mice", "rb" );
        fd = self.file.fileno()
        flag = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, flag | os.O_NONBLOCK)

    def getMouseEvent(self):
        try:
	  buf = self.file.read(3);
	  button = ord( buf[0] );
	  x,y = struct.unpack( "bb", buf[1:] );
          return bytearray(struct.pack('bbb', x, -1 * y, button))
        except IOError as e:
          return bytearray([0,0,0])

    def handle(self, bytes):
        self.tipi_io.send(self.getMouseEvent())
        return True

