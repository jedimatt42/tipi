import time
import logging

from Pab import *
from tipi.TipiPorts import TipiPorts

logger = logging.getLogger(__name__)


class UpgradeFile(object):
    @staticmethod
    def filename():
        return "UPGRADE"

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
        # Give the TI a little time to complete the IO request.
        time.sleep(1.000)
        with open("/tmp/tipiupgrade", "w") as fh_out:
            fh_out.write("woot")
        # Block forever, until we are killed and restarted.
        # by the TipiSuper service running the upgrade.
        while True:
            time.sleep(2)

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
