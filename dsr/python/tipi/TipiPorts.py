#!/usr/bin/env python
import RPi.GPIO as GPIO 
import sys

class TipiPorts(object):

    def __init__(self):
        self.__RESET = 5

        self.__TD0 = 2
        self.__TD1 = 3
        self.__TD2 = 4
        self.__TD3 = 17
        self.__TD4 = 27
        self.__TD5 = 22
        self.__TD6 = 10
        self.__TD7 = 9

        self.__TD_BITS = [self.__TD0, self.__TD1, self.__TD2, self.__TD3, self.__TD4, self.__TD5, self.__TD6, self.__TD7]

        self.__TC0 = 14
        self.__TC1 = 15
        self.__TC2 = 18
        self.__TC3 = 23
        self.__TC4 = 24
        self.__TC5 = 25
        self.__TC6 = 8
        self.__TC7 = 7

        self.__TC_BITS = [self.__TC0, self.__TC1, self.__TC2, self.__TC3, self.__TC4, self.__TC5, self.__TC6, self.__TC7]

        self.__R_CCLK = 19
        self.__R_DCLK = 26
        self.__R_SDATA = 13
        self.__R_LE = 6
 
        GPIO.setmode(GPIO.BCM) 
        GPIO.setwarnings(False)

        GPIO.setup(self.__RESET, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.__RESET, GPIO.FALLING, callback=onReset, bouncetime=100)

        GPIO.setup(self.__TD_BITS, GPIO.IN)
        GPIO.setup(self.__TC_BITS, GPIO.IN)

        GPIO.setup(self.__R_CCLK, GPIO.OUT)
        GPIO.setup(self.__R_DCLK, GPIO.OUT)
        GPIO.setup(self.__R_SDATA, GPIO.OUT)
        GPIO.setup(self.__R_LE, GPIO.OUT)

	self.setRD(0)
	self.setRC(0)
        GPIO.output(self.__R_CCLK, 0)
        GPIO.output(self.__R_DCLK, 0)
        GPIO.output(self.__R_SDATA, 0)
        GPIO.output(self.__R_LE, 0)

    #
    # Read a byte of input from a set of 8 input pins
    #
    def __readBitsToByte(self, bits):
        byte = 0

        # GPIO.input returns 1 or 0. so just shift them into place.
        byte += GPIO.input(bits[0]) # << 0
        byte += GPIO.input(bits[1]) << 1
        byte += GPIO.input(bits[2]) << 2
        byte += GPIO.input(bits[3]) << 3
        byte += GPIO.input(bits[4]) << 4
        byte += GPIO.input(bits[5]) << 5
        byte += GPIO.input(bits[6]) << 6
        byte += GPIO.input(bits[7]) << 7

        return byte

    #
    # Write a byte of to an 8 bit output register selected by clk
    #
    def __writeByteToRegister(self, byte, clk):
        for i in reversed(range(0,8)):
            GPIO.output(clk, 0)
            GPIO.output(self.__R_SDATA, (byte >> i) & 0x01)
            GPIO.output(clk, 1)
        
        GPIO.output(clk, 0)
        GPIO.output(self.__R_LE, 1)
        GPIO.output(clk, 1)
        GPIO.output(self.__R_LE, 0)
        GPIO.output(clk, 0)

    # Read TI_DATA
    def getTD(self):
        return self.__readBitsToByte(self.__TD_BITS)

    # Read TI_CONTROL
    def getTC(self):
        return self.__readBitsToByte(self.__TC_BITS)

    # Write RPI_DATA
    def setRD(self, value):
        self.__writeByteToRegister(value, self.__R_DCLK)

    # Write RPI_CONTROL
    def setRC(self, value):
        self.__writeByteToRegister(value, self.__R_CCLK)

def onReset(channel):
    print "responding to reset interrupt"
    sys.exit(0)


