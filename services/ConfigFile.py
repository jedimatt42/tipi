import os
import logging
from TipiConfig import TipiConfig
from Pab import *

LOGGER = logging.getLogger(__name__)


class ConfigFile(object):
    """ Special file PI.CONFIG for reading and writing tipi configuration """

    @staticmethod
    def filename():
        return "CONFIG"

    def __init__(self, tipi_io):
        self.tipi_io = tipi_io
        self.currentRecord = 0
        self.tipi_config = TipiConfig.instance()

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
        elif op == STATUS:
            self.status(pab, devname)
        else:
            self.tipi_io.send([EOPATTR])

    def close(self, pab, devname):
        self.tipi_config.save()
        self.tipi_io.send([SUCCESS])

    def open(self, pab, devname):
        if dataType(pab) == DISPLAY:
            if recordLength(pab) == 0 or recordLength(pab) == 80:
                self.currentRecord = 0
                self.tipi_config.load()
                self.tipi_io.send([SUCCESS])
                self.tipi_io.send([80])
                return
        self.tipi_io.send([EOPATTR])

    def read(self, pab, devname):
        if dataType(pab) == DISPLAY:
            if len(self.tipi_config.keys()) < (self.currentRecord + 1):
                self.tipi_io.send([EEOF])
                return
            key = self.tipi_config.keys()[self.currentRecord]
            value = self.tipi_config.get(key)
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
        self.tipi_config.set(key, value)
        self.tipi_io.send([SUCCESS])

    def status(self, pab, devname):
        self.tipi_io.send([SUCCESS])
        if len(self.tipi_config.keys()) < (self.currentRecord + 1):
            self.tipi_io.send([STVARIABLE | STLEOF])
            return
        self.tipi_io.send([STVARIABLE])

