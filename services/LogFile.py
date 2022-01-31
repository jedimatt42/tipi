import logging
import os
from Pab import *
from datetime import datetime
from subprocess import call

logger = logging.getLogger(__name__)


class LogFile(object):
    @staticmethod
    def filename():
        return "LOG"

    def __init__(self, tipi_io):
        self.tipi_io = tipi_io
        self.data_filename = None
        self.last_record = bytearray(0)

    def handle(self, pab, devname):
        op = opcode(pab)
        if op == OPEN:
            self.open(pab, devname)
        elif op == CLOSE:
            self.close(pab, devname)
        elif op == WRITE:
            self.write(pab, devname)
        elif op == READ:
            self.read(pab, devname)
        elif op == STATUS:
            self.status(pab, devname)
        else:
            self.tipi_io.send([EOPATTR])

    def close(self, pab, devname):
        self.tipi_io.send([SUCCESS])

    def open(self, pab, devname):
        if recordLength(pab) == 0 or recordLength(pab) == 80:
            self.tipi_io.send([SUCCESS])
            self.tipi_io.send([80])
            return
        else:
            reclen = recordLength(pab)
            self.tipi_io.send([SUCCESS])
            self.tipi_io.send([reclen])
            return

    def write(self, pab, devname):
        self.tipi_io.send([SUCCESS])
        data = self.tipi_io.receive()
        logger.info(str(data, 'latin1'));
        self.tipi_io.send([SUCCESS])

    def read(self, pab, devname):
        logger.info("read special? {}".format(devname))

    def status(self, pab, devname):
        logger.info("status special? {}".format(devname))

