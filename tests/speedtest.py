#!/usr/bin/env python
import sys
import time
import RPi.GPIO as GPIO 
from array import array
 
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

RD0 = 11
RD1 = 0
RD2 = 5
RD3 = 6
RD4 = 13
RD5 = 19
RD6 = 26
RD7 = 21

RD_BITS = [RD0, RD1, RD2, RD3, RD4, RD5, RD6, RD7]

RC0 = 1
RC1 = 12
RC2 = 16
RC3 = 20

RC_BITS = [RC0, RC1, RC2, RC3]
 
GPIO.setup(RD_BITS, GPIO.OUT)
GPIO.setup(RC_BITS, GPIO.OUT)

ACK_MASK = 0x03
 
#
# Return byte as string of bits: 0x40 => 01000000
#
def toBitString(byte):
    return bin(byte)[2:].zfill(8)

#
# Read a byte of input from a set of 8 input pins
#
def readTiByte(bits):
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
def writeTiByte(bits, byte):
    GPIO.output(bits[0], byte & 0x80)
    GPIO.output(bits[1], byte & 0x40)
    GPIO.output(bits[2], byte & 0x20)
    GPIO.output(bits[3], byte & 0x10)
    GPIO.output(bits[4], byte & 0x08)
    GPIO.output(bits[5], byte & 0x04)
    GPIO.output(bits[6], byte & 0x02)
    GPIO.output(bits[7], byte & 0x01)

#
# Write a byte of to a set of 8 output pins
#
def writeTiNibble(bits, byte):
    GPIO.output(bits[0], byte & 0x08)
    GPIO.output(bits[1], byte & 0x04)
    GPIO.output(bits[2], byte & 0x02)
    GPIO.output(bits[3], byte & 0x01)

#
# Write an array of bytes to TI
#
def writeBuffer(message):
    for byte in message:
        print byte
        next_syn = (readTiByte(TC_BITS) + 1) & ACK_MASK | 0x2
        print next_syn 
        writeTiByte(RD_BITS,byte)
        writeTiNibble(RC_BITS,next_syn)
        while next_syn != (readTiByte(TC_BITS) & ACK_MASK):
            time.sleep(0.002)
        print "received ack"
    
## 
## MAIN
##


writeTiNibble(RC_BITS,0x00)
while True:
    message = array('B',[0x11, 0x22, 0x33, 0x44, 0x55])
    writeBuffer(message)

 
