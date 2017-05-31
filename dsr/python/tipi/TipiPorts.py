import sys
import logging
import tipiports
import RPi.GPIO as GPIO

logger = logging.getLogger("tipi")

PIN_REG0 = 26
PIN_REG1 = 19
PIN_SHCLK = 4
PIN_SDATA_OUT = 13
PIN_SDATA_IN = 17
PIN_LE = 6

SEL_RD = 0
SEL_RC = 1
SEL_TD = 2
SEL_TC = 3

native = False

def wpi():
    return native

class TipiPorts(object):

    def __init__(self):
        if wpi():
            logger.info("Using libtipi wiringPi GPIO")
            tipiports.initGpio()
        else:
            logger.info("Using RPi.GPIO")
            tipigpio_init()
        logger.info("GPIO initialized.")


    # Read TI_DATA
    def getTD(self):
        if wpi():
            return tipiports.getTD()
        else:
            tipigpio_select(SEL_TD)
            return tipigpio_read()
            

    # Read TI_CONTROL
    def getTC(self):
        if wpi():
            return tipiports.getTC()
        else:
            tipigpio_select(SEL_TC)
            return tipigpio_read()

    # Write RPI_DATA
    def setRD(self, value):
        if wpi():
            tipiports.setRD(value)
        else:
            tipigpio_select(SEL_RD)
            tipigpio_write(value)

    # Write RPI_CONTROL
    def setRC(self, value):
        if wpi():
            tipiports.setRC(value)
        else:
            tipigpio_select(SEL_RD)
            tipigpio_write(value)

def tipigpio_init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(PIN_REG0, GPIO.OUT)
    GPIO.setup(PIN_REG1, GPIO.OUT)
    GPIO.setup(PIN_SHCLK, GPIO.OUT)
    GPIO.setup(PIN_SDATA_OUT, GPIO.OUT)
    GPIO.setup(PIN_LE, GPIO.OUT)
    GPIO.setup(PIN_SDATA_IN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.output(PIN_REG0, 0)
    GPIO.output(PIN_REG1, 0)
    GPIO.output(PIN_SHCLK, 0)
    GPIO.output(PIN_SDATA_OUT, 0)
    GPIO.output(PIN_LE, 0)

def tipigpio_select(reg):
    GPIO.output(PIN_REG0, reg & 0x02)
    GPIO.output(PIN_REG1, reg & 0x01)

def tipigpio_read():
    value = 0
    GPIO.output(PIN_LE, 1)
    GPIO.output(PIN_SHCLK, 1)
    GPIO.output(PIN_SHCLK, 0)
    GPIO.output(PIN_LE, 0)

    for i in reversed(range(0,8)):
        GPIO.output(PIN_SHCLK, 1)
        GPIO.output(PIN_SHCLK, 0)
        value += GPIO.input(PIN_SDATA_IN) << i

    return value

def tipigpio_write(value):
    for i in reversed(range(0,8)):
        GPIO.output(PIN_SDATA_OUT, (value >> i) & 0x01)
        GPIO.output(PIN_SHCLK, 1)
        GPIO.output(PIN_SHCLK, 0)
 
    GPIO.output(PIN_LE, 1)
    GPIO.output(PIN_SHCLK, 1)
    GPIO.output(PIN_SHCLK, 0)
    GPIO.output(PIN_LE, 0)



