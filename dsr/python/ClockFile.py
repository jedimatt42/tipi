
import time
from Pab import *


class ClockFile(object):

    @staticmethod
    def filename():
        return "TIPI.CLOCK"

    def __init__(self, tipi_io):
        self.tipi_io = tipi_io

    def handle(self, pab, devname):
        op = opcode(pab)
        if op == OPEN:
            self.open(pab, devname)
        elif op == CLOSE:
            self.close(pab, devname)
        elif op == READ:
            self.read(pab, devname)
        else:
            self.tipi_io.send([EOPATTR])

    def close(self, pab, devname):
        print "close special? {}".format(devname)
        self.tipi_io.send([SUCCESS])

    def open(self, pab, devname):
        if mode(pab) == INPUT:
            if dataType(pab) == DISPLAY:
                if recordLength(pab) == 0 or recordLength(pab) == 24:
                    self.tipi_io.send([SUCCESS])
                    self.tipi_io.send([24])
                    return
        self.tipi_io.send([EOPATTR])

    def read(self, pab, devname):
        if mode(pab) == INPUT:
            if dataType(pab) == DISPLAY:
                fdata = bytearray(time.asctime())
                self.tipi_io.send([SUCCESS])
                self.tipi_io.send(fdata)
                return
        self.tipi_io.send([EOPATTR])
