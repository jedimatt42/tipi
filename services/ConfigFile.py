
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
        self.records = {}
        self.sortedKeys = []

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
        with open(self.localpath, 'w') as fh:
            for key in self.sortedKeys:
                fh.write(key + "=" + self.records[key])
                fh.write("\n")
        self.tipi_io.send([SUCCESS])

    def open(self, pab, devname):
        if dataType(pab) == DISPLAY:
            if recordLength(pab) == 0 or recordLength(pab) == 80:
                self.currentRecord = 0
                self.records = {}
                if os.path.exists(self.localpath):
                    with open(self.localpath, 'r') as fh:
                        for line in fh.readlines():
                            key = line.split('=')[0].strip()
                            value = line.split('=')[1].strip()
                            self.records[key] = value
                            logger.debug("read record: %s = %s", key, value)
                else:
                    logger.info("config file missing: %s", self.localpath)
                self.sortedKeys = list(self.records.keys())
                self.sortedKeys.sort()
                self.tipi_io.send([SUCCESS])
                self.tipi_io.send([80])
                return
        self.tipi_io.send([EOPATTR])

    def read(self, pab, devname):
        if dataType(pab) == DISPLAY:
            if len(self.sortedKeys) < (self.currentRecord + 1):
                self.tipi_io.send([EEOF])
                return
            key = self.sortedKeys[self.currentRecord]
            value = self.records[key]
            msg = key + "=" + value
            self.tipi_io.send([SUCCESS])
            self.tipi_io.send(bytearray(msg))
            self.currentRecord += 1
            return
        self.tipi_io.send([EOPATTR])

    def write(self, pab, devname):
        self.tipi_io.send([SUCCESS])
        msg = str(self.tipi_io.receive())
        key = msg.split('=')[0].strip()
        value = msg.split('=')[1].strip()
        self.records[key] = value
        self.sortedKeys = list(self.records.keys())
        self.sortedKeys.sort()
        self.tipi_io.send([SUCCESS])

