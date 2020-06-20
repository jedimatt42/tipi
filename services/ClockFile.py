import time
import logging
from Pab import *

logger = logging.getLogger(__name__)


class ClockFile(object):
    @staticmethod
    def filename():
        return "CLOCK"

    def __init__(self, tipi_io):
        self.tipi_io = tipi_io
        self.mode = "corcomp"

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
        logger.info(f"close special? {devname}")
        self.tipi_io.send([SUCCESS])

    def open(self, pab, devname):
        if mode(pab) == INPUT or mode(pab) == UPDATE:
            if dataType(pab) == DISPLAY:
                if recordLength(pab) == 0 or recordLength(pab) == 19:
                    logger.info("clock mode:corcomp")
                    self.mode = "corcomp"
                    self.tipi_io.send([SUCCESS])
                    self.tipi_io.send([19])
                    return
                if recordLength(pab) == 24:
                    logger.info("clock mode:tipi")
                    self.mode = "tipi"
                    self.tipi_io.send([SUCCESS])
                    self.tipi_io.send([24])
                    return
        self.tipi_io.send([EOPATTR])

    def read(self, pab, devname):
        if mode(pab) == INPUT or mode(pab) == UPDATE:
            if dataType(pab) == DISPLAY:
                if self.mode == "corcomp":
                    pattern = "%w,%m/%d/%y,%H:%M:%S"
                    record = time.strftime(pattern)
                    fdata = bytearray(record, 'ascii')
                    self.tipi_io.send([SUCCESS])
                    self.tipi_io.send(fdata)
                    return
                if self.mode == "tipi":
                    record = time.asctime()
                    fdata = bytearray(record, 'ascii')
                    self.tipi_io.send([SUCCESS])
                    self.tipi_io.send(fdata)
                    return
        self.tipi_io.send([EOPATTR])
