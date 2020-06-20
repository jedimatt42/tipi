#!/usr/bin/env python
import sys
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

TD0 = 2
TD1 = 3
TD2 = 4
TD3 = 17
TD4 = 27
TD5 = 22
TD6 = 10
TD7 = 9

TD_BITS = [TD0, TD1, TD2, TD3, TD4, TD5, TD6, TD7]

TC0 = 14
TC1 = 15
TC2 = 18
TC3 = 23
TC4 = 24
TC5 = 25
TC6 = 8
TC7 = 7

TC_BITS = [TC0, TC1, TC2, TC3, TC4, TC5, TC6, TC7]

GPIO.setup(TD_BITS, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(TC_BITS, GPIO.IN, GPIO.PUD_UP)

#
# Read the D0-7 data bus GPIO pins and return as a byte.
#
def readTiByte(bits):
    byte = 0

    # GPIO.input returns 1 or 0. so just shift them into place.
    byte += GPIO.input(bits[0])  # << 0
    byte += GPIO.input(bits[1]) << 1
    byte += GPIO.input(bits[2]) << 2
    byte += GPIO.input(bits[3]) << 3
    byte += GPIO.input(bits[4]) << 4
    byte += GPIO.input(bits[5]) << 5
    byte += GPIO.input(bits[6]) << 6
    byte += GPIO.input(bits[7]) << 7

    return byte


while True:
    tc_data = readTiByte(TC_BITS)
    td_data = readTiByte(TD_BITS)
    print "TI Control: " + bin(tc_data)[2:].zfill(8) + " TI Data: " + bin(td_data)[
        2:
    ].zfill(8)
    time.sleep(0.2)  # just so my terminal is so busy.
