import sys
import logging
import time
import tipiports
#import RPi.GPIO as GPIO

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

#if __name__ == "__main__":
#    singleton.setRC(0x55)
#    singleton.setRD(0xAA)
#    print("test set M5FF9 = 0x55, M5FFB = 0xAA")
#    while True:
#        print("M5FFD = " + hex(singleton.getTC()) + " M5FFF = " + hex(singleton.getTD()))
#        time.sleep(5)

