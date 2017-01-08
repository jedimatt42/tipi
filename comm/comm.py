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

    byte += 1 if GPIO.input(BIT0) == True else 0
    byte += 2 if GPIO.input(BIT1) == True else 0
    byte += 4 if GPIO.input(BIT2) == True else 0
    byte += 8 if GPIO.input(BIT3) == True else 0
    byte += 16 if GPIO.input(BIT4) == True else 0
    byte += 32 if GPIO.input(BIT5) == True else 0
    byte += 64 if GPIO.input(BIT6) == True else 0
    byte += 128 if GPIO.input(BIT7) == True else 0

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

       
