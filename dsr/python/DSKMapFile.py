
import os
from Pab import *


class DSKMapFile(object):

    @staticmethod
    def filename():
        return "TIPI.DSKMAP"

    def __init__(self, tipi_io):
        self.tipi_io = tipi_io
        self.LINK = "/tipi_disk/DSK1"

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
        self.tipi_io.send([SUCCESS])

    def open(self, pab, devname):
        if dataType(pab) == DISPLAY:
            if recordLength(pab) == 0 or recordLength(pab) == 80:
                self.recordNo = 0
                self.tipi_io.send([SUCCESS])
                self.tipi_io.send([80])
                return
        self.tipi_io.send([EOPATTR])

    def read(self, pab, devname):
        if dataType(pab) == DISPLAY:
            if self.recordNo != 0:
                self.tipi_io.send([EEOF])
                return
            else:
                linkpath = os.path.basename(os.path.realpath(self.LINK))
                fdata = bytearray(linkpath)
                self.tipi_io.send([SUCCESS])
                self.tipi_io.send(fdata)
                self.recordNo += 1
                return
        self.tipi_io.send([EOPATTR])

    def write(self, pab, devname):
        self.tipi_io.send([SUCCESS])
        msg = str(self.tipi_io.receive())

        if os.path.exists(self.LINK):
            os.unlink(self.LINK)
        os.symlink("/tipi_disk/{}".format(msg), self.LINK)
