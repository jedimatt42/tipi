
import os
import logging
from Pab import *

logger = logging.getLogger(__name__)

class DSKMapFile(object):

    @staticmethod
    def filename():
        return "TIPI.DSKMAP"

    def __init__(self, tipi_io):
        self.tipi_io = tipi_io
        self.LINK = "/home/tipi/tipi_disk/DSK"

    def handle(self, pab, devname):
        logPab(pab)
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
            if self.recordNo < 0 or self.recordNo > 2:
                self.tipi_io.send([EEOF])
                return
            else:
                dsk = self.recordNo + 1
                linkpath = os.path.basename(os.path.realpath(self.LINK + str(dsk)))
                fdata = bytearray(linkpath)
                self.tipi_io.send([SUCCESS])
                self.tipi_io.send(fdata)
                self.recordNo += 1
                return
        self.tipi_io.send([EOPATTR])

    def write(self, pab, devname):
        self.tipi_io.send([SUCCESS])
        try:
            msg = str(self.tipi_io.receive()).rstrip()
            logger.debug("setting link to \"%s\"", msg)
            self.recordNo = recordNumber(pab)
            link = self.LINK + str(self.recordNo)
            if os.path.lexists(link):
                logger.info("removing symlink %s", link)
                os.unlink(link)
            else:
                logger.info("link did not exist %s", link)
            if msg != "DSK{}".format(self.recordNo):
                logger.info("creating symlink for mapping %s", link)
                os.symlink("/home/tipi/tipi_disk/{}".format(msg), link)
            self.tipi_io.send([SUCCESS])
        except Exception as e:
            logger.exception("Failed to create %s link", link)
            self.tipi_io.send([EFILERR])
