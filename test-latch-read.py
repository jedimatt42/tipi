#!/usr/bin/env python
import sys
import time
import RPi.GPIO as GPIO 
 
GPIO.setmode(GPIO.BCM) 
GPIO.setwarnings(False)
 
BIT0 = 17
BIT1 = 4
BIT2 = 22
BIT3 = 18
BIT4 = 23
BIT5 = 24
BIT6 = 25
BIT7 = 27
 
GPIO.setup(BIT0, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(BIT1, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(BIT2, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(BIT3, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(BIT4, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(BIT5, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(BIT6, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(BIT7, GPIO.IN, GPIO.PUD_UP)
 
while True:
 
    if GPIO.input(BIT0) == False:
        sys.stdout.write("0")
    else:
        sys.stdout.write("1")
 
    if GPIO.input(BIT1) == False:
        sys.stdout.write("0")
    else:
        sys.stdout.write("1")
 
 
    if GPIO.input(BIT2) == False:
        sys.stdout.write("0")
    else:
        sys.stdout.write("1")
 
 
    if GPIO.input(BIT3) == False:
        sys.stdout.write("0")
    else:
        sys.stdout.write("1")
 
 
    if GPIO.input(BIT4) == False:
        sys.stdout.write("0")
    else:
        sys.stdout.write("1")
 
 
    if GPIO.input(BIT5) == False:
        sys.stdout.write("0")
    else:
        sys.stdout.write("1")
 
 
    if GPIO.input(BIT6) == False:
        sys.stdout.write("0")
    else:
        sys.stdout.write("1")
 
 
    if GPIO.input(BIT7) == False:
        sys.stdout.write("0")
    else:
        sys.stdout.write("1")
 
 
    print ("\n")