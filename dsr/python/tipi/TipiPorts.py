import sys
import logging
import time
import tipiports
import RPi.GPIO as GPIO

logger = logging.getLogger(__name__)

class TipiPorts(object):

    def __init__(self):
        logger.info("Using libtipi wiringPi GPIO")
        tipiports.initGpio()
        self.setRD(0)
        self.setRC(0)
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

    # Use this method to make sure we only
    @staticmethod
    def getInstance():
        return singleton

singleton = TipiPorts()
