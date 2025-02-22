import logging

from Pab import (
    opcode, recordLength,
    EOPATTR, SUCCESS,
    OPEN, CLOSE, READ, WRITE,
)
from CustomExtensions import CustomExtensions

logger = logging.getLogger(__name__)


class MsgFile(object):

    @staticmethod
    def filename():
        # open file in "append" mode, such as:
        #   PI.MSG
        return "MSG"

    def __init__(self, tipi_io):
        self.tipi_io = tipi_io
        self.custom_extensions = CustomExtensions(tipi_io)
        self.last_response = []

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
        logger.info("close devname: %s", devname)
        self.tipi_io.send([SUCCESS])

    def open(self, pab, devname):
        logger.debug("open devname: %s", devname)
        recLen = recordLength(pab)
        if recLen == 0:
            recLen = 80
        self.tipi_io.send([SUCCESS])
        self.tipi_io.send([recLen])
        return

    def read(self, pab, devname):
        logger.info("read devname: %s", devname)
        self.tipi_io.send([SUCCESS])
        self.tipi_io.send(self.last_response)
        return

    def write(self, pab, devname):
        logger.info("write devname: %s", devname)
        self.tipi_io.send([SUCCESS])
        data = self.tipi_io.receive()
        self.last_response = self.custom_extensions.processRequest(data)
        self.tipi_io.send([SUCCESS])

