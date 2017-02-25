#!/usr/bin/env python
import sys
import time
import RPi.GPIO as GPIO 
from array import array
 
GPIO.setmode(GPIO.BCM) 
GPIO.setwarnings(True)

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
 
GPIO.setup(TD_BITS, GPIO.IN)
GPIO.setup(TC_BITS, GPIO.IN)

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

RESET = 0x01
 
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

# Read TI_DATA
def getTD():
    return readTiByte(TD_BITS)

# Read TI_CONTROL
def getTC():
    return readTiByte(TC_BITS)

# Write RPI_DATA
def setRD(value):
    writeTiByte(RD_BITS, value)

# Write RPI_CONTROL
def setRC(value):
    writeTiNibble(RC_BITS, value)

#
# Debugging output, to show currently available bits
#
def logInputs():
    sys.stdout.write( hex(readTiByte(TD_BITS))[2:].zfill(2) + " - " + hex(readTiByte(TC_BITS))[2:].zfill(2) )
    sys.stdout.write( '\r' )
    sys.stdout.flush()


prev_syn = RESET

#
# Block until both sides show control bits reset
# The TI resets first, and then RPi responds
#
def resetProtocol():
    global prev_syn
    print "waiting for reset..."
    # And wait for the TI to signal RESET
    while getTC() != RESET:
        logInputs()
        pass
    # Reset the control signals
    setRD(0x00)
    setRC(RESET)
    prev_syn = RESET
    print "reset complete"

#
# transmit a byte when TI requests it
def sendByte(byte):
    global prev_syn
    next_ack = prev_syn
    while prev_syn == next_ack:
        logInputs()
        prev_syn = getTC()
        # TODO: should be validating that it was a read request from the TI.
    next_ack = prev_syn
    setRD(byte)
    setRC(next_ack & ACK_MASK)

#
# block until byte is received.
def receiveByte():
    global prev_syn
    next_ack = prev_syn
    while prev_syn == next_ack:
        logInputs()
        prev_syn = getTC()
    next_ack = prev_syn
    val = getTD()
    setRC(next_ack & ACK_MASK)
    return val

#
# PAB routines...
#

#
# Return the TI DSR Opcode
def opcode(pab):
    return pab[0]

#
# Return byte count from PAB / or byte count in LOAD/SAVE operations
def recordNumber(pab):
    return pab[6] << 8 + pab[7];

#
# Opcode Handling
#

EDVNAME=0x00
EWPROT=0x01
EOPATTR=0x02
EILLOP=0x03
ENOSPAC=0x04
EEOF=0x05
EDEVERR=0x06
EFILERR=0x07

def handleNotSupported(pab, devname):
    print "Opcode not supported: " + str(opcode(pab))
    sendErrorCode(EILLOP)

def sendErrorCode(code):
    print "responding with error: " + str(code)
    sendByte(code)

def handleLoad(pab, devname):
    print "LOADing " + str(devname)
    sendErrorCode(EFILERR)
    
## 
## MAIN
##

# Initial device state.
setRD(0x00)
setRC(0x00)

while True:
    print "Ready for request..."
    resetProtocol()

    pab = bytearray(10)
    for i in range(0,10):
        pab[i] = receiveByte()
	print "PAB[" + str(i) + "]: " + hex(pab[i])

    resetProtocol()

    devicename = bytearray(pab[9])
    for i in range(0,pab[9]):
        devicename[i] = receiveByte()
        print "devname[" + str(i) + "]: " + chr(devicename[i])

    switcher = {
	5: handleLoad
    }

    # every path from here is a response back, so switching flags requires a reset in-between
    resetProtocol()

    handler = switcher.get(opcode(pab), handleNotSupported)
    handler(pab, devicename)

    print "Request completed."


