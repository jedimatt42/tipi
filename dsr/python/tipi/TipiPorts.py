#!/usr/bin/env python
# import RPi.GPIO as GPIO 
import sys
import logging
import tipiports

logger = logging.getLogger("tipi")

class TipiPorts(object):

    def __init__(self):
        self.__RESET = 5

        tipiports.initGpio()

        # GPIO.setmode(GPIO.BCM) 
        # GPIO.setwarnings(False)

        # GPIO.setup(self.__RESET, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # Do not proceed unless the reset signal has turned off
        # attempt to prevent restart storm in systemd
        
        # while GPIO.input(self.__RESET) != 1:
        #     logger.info("waiting for reset to complete.")
        #     pass
        # GPIO.add_event_detect(self.__RESET, GPIO.FALLING, callback=onReset, bouncetime=100)
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

def onReset(channel):
    print "responding to reset interrupt"
    sys.exit(0)


