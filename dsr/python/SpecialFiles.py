
import time
from Pab import *

class SpecialFiles(object):

    def __init__(self, tipi_io):
        self.tipi_io = tipi_io

    def open(self, pab, devname):
        print "open special? {}".format(devname)
        if devname == "TIPI.CLOCK" and mode(pab) == INPUT:
            if dataType(pab) == DISPLAY:
                if recordLength(pab) == 0 or recordLength(pab) == 24:
                    self.tipi_io.send([SUCCESS])
                    self.tipi_io.send([24])
                    print "CLOCK opened successfully"
                    return True
                else:
                    self.tipi_io.send([EOPATTR])
                    print "CLOCK opened with bad pattern"
                    return True
                    
        return False

    def read(self, pab, devname):
        print "read special? {}".format(devname)
        if devname == "TIPI.CLOCK" and mode(pab) == INPUT:
            if dataType(pab) == DISPLAY:
                fdata = bytearray(time.asctime())
                self.tipi_io.send([SUCCESS])
                self.tipi_io.send(fdata)
                return True
        return False



