#!/usr/bin/env python
import sys
import time
import RPi.GPIO as GPIO 
 
GPIO.setmode(GPIO.BCM) 
GPIO.setwarnings(False)
 
BIT0 = 19
BIT1 = 13
BIT2 = 6
BIT3 = 5
BIT4 = 22
BIT5 = 27
BIT6 = 17
BIT7 = 4
 
GPIO.setup(BIT0, GPIO.OUT)
GPIO.setup(BIT1, GPIO.OUT)
GPIO.setup(BIT2, GPIO.OUT)
GPIO.setup(BIT3, GPIO.OUT)
GPIO.setup(BIT4, GPIO.OUT)
GPIO.setup(BIT5, GPIO.OUT)
GPIO.setup(BIT6, GPIO.OUT)
GPIO.setup(BIT7, GPIO.OUT)
 
value = 0x1F

GPIO.output(BIT0, value & 0x01)
GPIO.output(BIT1, value & 0x02)
GPIO.output(BIT2, value & 0x04)
GPIO.output(BIT3, value & 0x08)
GPIO.output(BIT4, value & 0x10)
GPIO.output(BIT5, value & 0x20)
GPIO.output(BIT6, value & 0x40)
GPIO.output(BIT7, value & 0x80)
 
while True:
    True


