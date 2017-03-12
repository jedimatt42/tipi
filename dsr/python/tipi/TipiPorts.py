#!/usr/bin/env python
import RPi.GPIO as GPIO 

class TipiPorts(object):

    def __init__(self):
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
 
        self.__RD0 = 11
        self.__RD1 = 0
        self.__RD2 = 5
        self.__RD3 = 6
        self.__RD4 = 13
        self.__RD5 = 19
        self.__RD6 = 26
        self.__RD7 = 21

        self.__RD_BITS = [self.__RD0, self.__RD1, self.__RD2, self.__RD3, self.__RD4, self.__RD5, self.__RD6, self.__RD7]

        self.__RC0 = 1
        self.__RC1 = 12
        self.__RC2 = 16
        self.__RC3 = 20

        self.__RC_BITS = [self.__RC0, self.__RC1, self.__RC2, self.__RC3]
 
        GPIO.setmode(GPIO.BCM) 
        GPIO.setwarnings(True)

        GPIO.setup(self.__TD_BITS, GPIO.IN)
        GPIO.setup(self.__TC_BITS, GPIO.IN)

        GPIO.setup(self.__RD_BITS, GPIO.OUT)
        GPIO.setup(self.__RC_BITS, GPIO.OUT)

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
    # Write a byte of to a set of 8 output pins
    #
    def __writeByteToBits(self, byte, bits):
        GPIO.output(bits[0], byte & 0x80)
        GPIO.output(bits[1], byte & 0x40)
        GPIO.output(bits[2], byte & 0x20)
        GPIO.output(bits[3], byte & 0x10)
        GPIO.output(bits[4], byte & 0x08)
        GPIO.output(bits[5], byte & 0x04)
        GPIO.output(bits[6], byte & 0x02)
        GPIO.output(bits[7], byte & 0x01)

    #
    # Write a least significant 4 bits of a byte to a set of 4 output pins
    #
    def __writeNibbleToBits(self, byte, bits):
        GPIO.output(bits[0], byte & 0x08)
        GPIO.output(bits[1], byte & 0x04)
        GPIO.output(bits[2], byte & 0x02)
        GPIO.output(bits[3], byte & 0x01)

    # Read TI_DATA
    def getTD(self):
        return self.__readBitsToByte(self.__TD_BITS)

    # Read TI_CONTROL
    def getTC(self):
        return self.__readBitsToByte(self.__TC_BITS)

    # Write RPI_DATA
    def setRD(self, value):
        self.__writeByteToBits(value, self.__RD_BITS)

    # Write RPI_CONTROL
    def setRC(self, value):
        self.__writeNibbleToBits(value, self.__RC_BITS)

