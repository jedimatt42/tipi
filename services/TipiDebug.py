#!/usr/bin/env python3
from tipi.TipiPorts import TipiPorts
import RPi.GPIO as GPIO
import time

##
## For instructions see LOW_LEVEL_TESTING.md
##

PIN_R_RT=13
PIN_R_CD=21
PIN_R_CLK=6
PIN_R_DOUT=16
PIN_R_DIN=20
PIN_R_LE=19

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_R_RT, GPIO.OUT)
    GPIO.setup(PIN_R_CD, GPIO.OUT)
    GPIO.setup(PIN_R_CLK, GPIO.OUT)
    GPIO.setup(PIN_R_DOUT, GPIO.OUT)
    GPIO.setup(PIN_R_LE, GPIO.OUT)
    GPIO.setup(PIN_R_DIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.output(PIN_R_RT, 0)
    GPIO.output(PIN_R_CD, 0)
    GPIO.output(PIN_R_CLK, 0)
    GPIO.output(PIN_R_DOUT, 0)
    GPIO.output(PIN_R_LE, 0)
    

def setSelect(reg):
    GPIO.output(PIN_R_RT, (reg & 0x02) >> 1);
    GPIO.output(PIN_R_CD, reg & 0x01);
    time.sleep(0.01)


def writeReg(reg, value):
    setSelect(reg)
    i=7
    while i >= 0:
        GPIO.output(PIN_R_DOUT, (value >> i) & 0x01)
        time.sleep(0.01)
        GPIO.output(PIN_R_CLK, 1)
        time.sleep(0.01)
        GPIO.output(PIN_R_CLK, 0)
        time.sleep(0.01)
        i=i-1
    GPIO.output(PIN_R_LE, 1)
    time.sleep(0.01)
    GPIO.output(PIN_R_CLK, 1)
    time.sleep(0.01)
    GPIO.output(PIN_R_CLK, 0)
    time.sleep(0.01)
    GPIO.output(PIN_R_LE, 0)
    time.sleep(0.01)


def readReg(reg):
    value = 0
    setSelect(reg)

    GPIO.output(PIN_R_LE, 1)
    time.sleep(0.01)
    GPIO.output(PIN_R_CLK, 1)
    time.sleep(0.01)
    GPIO.output(PIN_R_CLK, 0)
    time.sleep(0.01)
    GPIO.output(PIN_R_LE, 0)
    time.sleep(0.01)

    i=7
    while i >= 0:
        GPIO.output(PIN_R_CLK, 1)
        time.sleep(0.01)
        GPIO.output(PIN_R_CLK, 0)
        time.sleep(0.01)
        value |= GPIO.input(PIN_R_DIN) << i
        i=i-1

    GPIO.output(PIN_R_CLK, 1)
    time.sleep(0.01)
    GPIO.output(PIN_R_CLK, 0)
    time.sleep(0.01)
    GPIO.input(PIN_R_DIN)
    time.sleep(0.01)
    return value


SEL_RC=0
SEL_RD=1
SEL_TC=2
SEL_TD=3

setup()
# write 55 to 5ff9, and AA to 5ffb
rc = 0x5A
rd = 0xA5
writeReg(SEL_RC,rc)
writeReg(SEL_RD,rd)
print(f"wrote m5FF9: {hex(rc)} m5FFB: {hex(rd)}")

# then read 5ffd and 5fff and print the values
while True:
    tc = readReg(SEL_TC)
    td = readReg(SEL_TD)
    print(f"read m5FFD: {hex(tc)} m5FFF: {hex(td)}")
    time.sleep(5)

