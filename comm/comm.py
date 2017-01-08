#!/usr/bin/env python
import sys
import time
import RPi.GPIO as GPIO 
 
GPIO.setmode(GPIO.BCM) 
GPIO.setwarnings(False)
 
state = 0

BIT0 = 19
BIT1 = 13
BIT2 = 6
BIT3 = 5
BIT4 = 22
BIT5 = 27
BIT6 = 17
BIT7 = 4

BITS = [BIT0, BIT1, BIT2, BIT3, BIT4, BIT5, BIT6, BIT7]
 
GPIO.setup(BITS, GPIO.IN, GPIO.PUD_UP)
 
#
# Read the D0-7 data bus GPIO pins and return as a byte.
#
def readTiByte():
    byte = 0

    # GPIO.input returns 1 or 0. so just shift them into place.
    byte += GPIO.input(BIT0) # << 0
    byte += GPIO.input(BIT1) << 1
    byte += GPIO.input(BIT2) << 2
    byte += GPIO.input(BIT3) << 3
    byte += GPIO.input(BIT4) << 4
    byte += GPIO.input(BIT5) << 5
    byte += GPIO.input(BIT6) << 6
    byte += GPIO.input(BIT7) << 7

    return byte

#
# Send a byte to the tty, handling CR -> CR/LF translation.
#
def writeChar(byte):
    sys.stdout.write(chr(byte))
    if byte == 13:
        sys.stdout.write("\n")
    sys.stdout.flush()


# Now loop over input and copy to terminal...

while True:
    byte = readTiByte()

    if byte == 1:
    	state = 1
	time.sleep(.002)

    elif state == 1 and byte != 1:
        writeChar(byte)
        state = 0

       
