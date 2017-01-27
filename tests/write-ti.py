#!/usr/bin/env python
import sys
import time
import RPi.GPIO as GPIO 
 
GPIO.setmode(GPIO.BCM) 
GPIO.setwarnings(False)
 
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
 
value = 0x1F

GPIO.output(RD0, value & 0x80)
GPIO.output(RD1, value & 0x40)
GPIO.output(RD2, value & 0x20)
GPIO.output(RD3, value & 0x10)
GPIO.output(RD4, value & 0x08)
GPIO.output(RD5, value & 0x04)
GPIO.output(RD6, value & 0x02)
GPIO.output(RD7, value & 0x01)

rc_val = 0x0A
GPIO.output(RC0, rc_val & 0x08)
GPIO.output(RC1, rc_val & 0x04)
GPIO.output(RC2, rc_val & 0x02)
GPIO.output(RC3, rc_val & 0x01)

 
while True:
    True


