import struct

# Issues: reading from file is blocking IO. 
# Can't be blocking the TI-99/4A like that. 

class Mouse(object):

    def __init__(self, tipi_io):
        self.tipi_io = tipi_io
        self.file = open( "/dev/input/mice", "rb" );

    def getMouseEvent(self):
	buf = self.file.read(3);
	button = ord( buf[0] );
	# bLeft = button & 0x1;
	# bMiddle = ( button & 0x4 ) > 0;
	# bRight = ( button & 0x2 ) > 0;
	x,y = struct.unpack( "bb", buf[1:] );
        # Probably could just skip the unpack and accept button as first byte.
        return bytearray(struct.pack('bbb', x, -1 * y, button))

    def handle(self, bytes):
        self.tipi_io.sendRaw(self.getMouseEvent())
        return True

