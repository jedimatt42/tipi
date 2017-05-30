import sys
import logging
import tipiports

logger = logging.getLogger("tipi")

class TipiPorts(object):

    def __init__(self):
        tipiports.initGpio()
        logger.info("GPIO initialized.")


    # Read TI_DATA
    def getTD(self):
        return tipiports.getTD()

    # Read TI_CONTROL
    def getTC(self):
        return tipiports.getTC()

    # Write RPI_DATA
    def setRD(self, value):
        tipiports.setRD(value)

    # Write RPI_CONTROL
    def setRC(self, value):
        tipiports.setRC(value)


