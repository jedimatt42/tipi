
import time
import logging

from Pab import *

logger = logging.getLogger(__name__)


class ShutdownFile(object):

    @staticmethod
    def filename():
        return "SHUTDOWN"

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
        elif op == STATUS:
            self.status(pab, devname)
        else:
            logger.warn("Unhandled opcode %d for %s", op, devname)
            self.tipi_io.send([EOPATTR])

    def close(self, pab, devname):
        logger.info("close %s", devname)
        self.tipi_io.send([SUCCESS])
        with open("/tmp/tipihalt", 'w') as fh_out:
            fh_out.write("woot")

    def open(self, pab, devname):
        logger.info("open %s", devname)
        self.tipi_io.send([SUCCESS])
        self.tipi_io.send([80])

    def read(self, pab, devname):
        logger.info("read %s", devname)
        self.tipi_io.send([EEOF])

    def status(self, pab, devname):
        logger.info("status %s", devname)
        if mode(pab) == INPUT:
            if dataType(pab) == DISPLAY:
                self.tipi_io.send([SUCCESS])
                statbyte = STVARIABLE
                statbyte |= STLEOF
                self.tipi_io.send([statbyte])
                return
        self.tipi_io.send([EOPATTR])
