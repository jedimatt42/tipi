
import os
import logging
from Pab import *

logger = logging.getLogger(__name__)

class ConfigFile(object):

    @staticmethod
    def filename():
        return "CONFIG"

    def __init__(self, tipi_io):
        self.tipi_io = tipi_io
        self.localpath = "/home/tipi/tipi.config"
        self.currentRecord = 0

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
        with open(self.localpath,'w') as fh:
            for line in self.records:
                fh.write(line)
                fh.write("\n")
        self.tipi_io.send([SUCCESS])

    def open(self, pab, devname):
        if dataType(pab) == DISPLAY:
            if recordLength(pab) == 0 or recordLength(pab) == 80:
                self.currentRecord = 0
                self.records = []
                if os.path.exists(self.localpath):
                    with open(self.localpath,'r') as fh:
                        for line in fh.readlines():
                            self.records += [line.rstrip()]
                self.tipi_io.send([SUCCESS])
                self.tipi_io.send([80])
                return
        self.tipi_io.send([EOPATTR])

    def read(self, pab, devname):
        if dataType(pab) == DISPLAY:
            self.tipi_io.send([EEOF])
        self.tipi_io.send([EOPATTR])

    def write(self, pab, devname):
        self.tipi_io.send([SUCCESS])
        msg = str(self.tipi_io.receive()).rstrip()
        try:
            recNo = recordNumber(pab)
            if recNo != 0:
                self.currentRecord = recNo
            if self.currentRecord >= len(self.records):
                self.records += [bytearray(0)] * (1 + self.currentRecord - len(self.records))
            self.records[self.currentRecord] = msg
            self.currentRecord += 1
            self.tipi_io.send([SUCCESS])
        except Exception as e:
            logger.exception(e)
            self.tipi_io.send([EFILERR])

