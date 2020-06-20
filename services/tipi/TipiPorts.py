import sys
import logging
import time
import tipiports

logger = logging.getLogger(__name__)


class TipiPorts(object):
    def __init__(self):
        logger.info("Using libtipi wiringPi GPIO")
        tipiports.initGpio()
        logger.info("GPIO initialized.")

    # Send whole message
    def sendMsg(self, data):
        tipiports.sendMsg(data)

    # Receive whole message
    def readMsg(self):
        return tipiports.readMsg()

    # Use this method to make sure we only
    @staticmethod
    def getInstance():
        return singleton


singleton = TipiPorts()
