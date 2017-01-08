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


 
GPIO.setup(BIT0, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(BIT1, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(BIT2, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(BIT3, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(BIT4, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(BIT5, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(BIT6, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(BIT7, GPIO.IN, GPIO.PUD_UP)
 
while True:

    byte = 0

    byte += GPIO.input(BIT0) # << 0
    byte += GPIO.input(BIT1) << 1
    byte += GPIO.input(BIT2) << 2
    byte += GPIO.input(BIT3) << 3
    byte += GPIO.input(BIT4) << 4
    byte += GPIO.input(BIT5) << 5
    byte += GPIO.input(BIT6) << 6
    byte += GPIO.input(BIT7) << 7

#    print byte

    if byte == 1:
#        sys.stdout.write(".")
    	state = 1
	time.sleep(.002)
#        sys.stdout.write(".")

    elif state == 1 and byte != 1:
#       print chr(byte)
#       print byte
       sys.stdout.write(chr(byte)) 

       if byte == 13:
           sys.stdout.write("\n")

       sys.stdout.flush()
#       print "dsf"
       state = 0

       
