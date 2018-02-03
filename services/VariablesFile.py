import logging
from TipiVariable import TipiVariable

from Pab import *

logger = logging.getLogger(__name__)


class VariablesFile(object):

    @staticmethod
    def filename():
        # open file in "update" mode, such as:
        #   PI.VARS, write a command, then read the response as a Display Variable 254 file from BASIC
        return "VARS"

    def __init__(self, tipi_io):
        self.tipi_io = tipi_io
        self.lastResponse = None
        self.vars = None

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
        logger.debug("close devname: %s", devname)
        self.lastResponse = None
        self.vars = None
        self.tipi_io.send([SUCCESS])

    def open(self, pab, devname):
        logger.debug("open devname: %s", devname)
        self.lastResponse = None
        self.vars = TipiVariable(self.tipi_io)
        self.tipi_io.send([SUCCESS])
        self.tipi_io.send([254])

    def write(self, pab, devname):
        logger.debug("write devname: %s", devname)
        lastResponse = None
        self.tipi_io.send([SUCCESS])
        msg = self.tipi_io.receive()
        try:
            self.lastResponse = self.vars.processRequest(msg)
            self.tipi_io.send([SUCCESS])
        except Exception as e:
            logger.error("Failure in TipiVariable processing")
            self.tipi_io.send([EFILERR])

    def read(self, pab, devname):
        logger.debug("read devname: %s", devname)
        if not self.lastResponse is None:
            fdata = bytearray(self.lastResponse)
            self.tipi_io.send([SUCCESS])
            self.tipi_io.send(fdata)
            return
        self.tipi_io.send([EFILERR])


