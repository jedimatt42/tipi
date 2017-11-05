
import time
import logging
from Pab import *
from Status import Status

logger = logging.getLogger(__name__)


class StatusFile(object):

    @staticmethod
    def filename():
        return "STATUS"

    def __init__(self, tipi_io):
        self.tipi_io = tipi_io
        self.tipiStatus = []
        self.recordNo = 0

    def getRecNo(self, pab):
        readRec = recordNumber(pab)
        if readRec != 0:
            self.recordNo = readRec
        return self.recordNo

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

    def open(self, pab, devname):
        logger.info("open %s", devname)
        if mode(pab) == INPUT:
            if dataType(pab) == DISPLAY:
                if recordLength(pab) == 0 or recordLength(pab) == 80:
                    self.tipi_io.send([SUCCESS])
                    self.tipi_io.send([80])
                    self.tipiStatus = Status()
                    self.recordNo = 0
                    return
        self.tipi_io.send([EOPATTR])

    def read(self, pab, devname):
        logger.info("read %s", devname)
        if mode(pab) == INPUT:
            if dataType(pab) == DISPLAY:
                readRec = self.getRecNo(pab)

                if readRec >= self.tipiStatus.len():
                    self.tipi_io.send([EEOF])
                    return
                else:
                    fdata = bytearray(self.tipiStatus.record(readRec))
                    self.tipi_io.send([SUCCESS])
                    self.tipi_io.send(fdata)
                    self.recordNo += 1
                    return
        self.tipi_io.send([EOPATTR])

    def status(self, pab, devname):
        logger.info("status %s", devname)
        if mode(pab) == INPUT:
            if dataType(pab) == DISPLAY:
                self.tipi_io.send([SUCCESS])
                statbyte = STVARIABLE
                readRec = self.getRecNo(pab)
                if readRec >= self.tipiStatus.len():
                    statbyte |= STLEOF
                self.tipi_io.send([statbyte])
                return
        self.tipi_io.send([EOPATTR])
