#!/usr/bin/env python
import sys
import time
import RPi.GPIO as GPIO 
from array import array
import re
from ti_files import ti_files

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

RESET = 0x01
TSWB = 0x02
TSRB = 0x06
ACK_MASK = 0x03
 
#
# Read a byte of input from a set of 8 input pins
#
def readBitsToByte(bits):
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
def writeByteToBits(byte, bits):
    GPIO.output(bits[0], byte & 0x80)
    GPIO.output(bits[1], byte & 0x40)
    GPIO.output(bits[2], byte & 0x20)
    GPIO.output(bits[3], byte & 0x10)
    GPIO.output(bits[4], byte & 0x08)
    GPIO.output(bits[5], byte & 0x04)
    GPIO.output(bits[6], byte & 0x02)
    GPIO.output(bits[7], byte & 0x01)

#
# Write a least significant 4 bits of a byte to a set of 4 output pins
#
def writeNibbleToBits(byte, bits):
    GPIO.output(bits[0], byte & 0x08)
    GPIO.output(bits[1], byte & 0x04)
    GPIO.output(bits[2], byte & 0x02)
    GPIO.output(bits[3], byte & 0x01)

# Read TI_DATA
def getTD():
    return readBitsToByte(TD_BITS)

# Read TI_CONTROL
def getTC():
    return readBitsToByte(TC_BITS)

# Write RPI_DATA
def setRD(value):
    writeByteToBits(value, RD_BITS)

# Write RPI_CONTROL
def setRC(value):
    writeNibbleToBits(value, RC_BITS)

#
# Debugging output, to show currently available bits
#
def logInputs(expected):
    #sys.stdout.write( "\t\t\t" + hex(getTD())[2:].zfill(2) + " - " + hex(getTC())[2:].zfill(2) + " - exp: " + hex(expected)[2:].zfill(2) )
    #sys.stdout.write( '\r' )
    #sys.stdout.flush()
    #time.sleep(0.1)
    pass


prev_syn = 0

#
# Block until both sides show control bits reset
# The TI resets first, and then RPi responds
#
def resetProtocol():
    global prev_syn
    print "waiting for reset..."
    # And wait for the TI to signal RESET
    prev_syn = 0
    while prev_syn != RESET:
        logInputs(RESET)
        prev_syn = getTC()
    # Reset the control signals
    setRC(RESET)
    print "reset complete"

#
# change mode to sending bytes
def modeSend():
    global prev_syn
    # actual send calls will always pre-increment this, so we start a series by making sure the low bit will increment to zero.
    prev_syn = TSRB + 1

#
# transmit a byte when TI requests it
def sendByte(byte):
    global prev_syn
    next_syn = ((prev_syn + 1) & ACK_MASK) | TSRB
    while prev_syn != next_syn:
        logInputs(next_syn)
        prev_syn = getTC()
    setRD(byte)
    setRC(prev_syn & ACK_MASK)
    # print "sent byte: " + hex(byte)[2:].zfill(2)

#
# change mode to sending bytes
def modeRead():
    global prev_syn
    # actual send calls will always pre-increment this, so we start a series by making sure the low bit will increment to zero.
    prev_syn = TSWB + 1

#
# block until byte is received.
def readByte():
    global prev_syn
    next_syn = ((prev_syn + 1) & ACK_MASK) | TSWB
    while prev_syn != next_syn:
        logInputs(next_syn)
        prev_syn = getTC()
    next_ack = prev_syn
    val = getTD()
    setRC(prev_syn & ACK_MASK)
    return val

#
# PAB routines...
#

#
# Return the TI DSR Opcode
def opcode(pab):
    return int(pab[0])

#
# Return byte count from PAB / or byte count in LOAD/SAVE operations
def recordNumber(pab):
    return (pab[6] << 8) + pab[7];

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

SUCCESS=0xFF

def handleNotSupported(pab, devname):
    print "Opcode not supported: " + str(opcode(pab))
    sendErrorCode(EILLOP)

def sendErrorCode(code):
    print "responding with error: " + str(code)
    sendByte(code)

def deviceToFilename(devname):
    pattern = re.compile('[^\.]+')
    tokens = pattern.findall(str(devname))
    # cheating
    return "/tipi_disk/" + tokens[1]

def handleLoad(pab, devname):
    print "Opcode 5 LOAD - " + str(devname)
    maxsize = recordNumber(pab)
    print "\tmax bytes: " + str(maxsize)
    unix_name = deviceToFilename(devname)
    print "\tunix_name: " + unix_name
    fh = None
    try:
        fh = open(unix_name, 'rb')
        bytes = bytearray(fh.read())
        # TODO: check that it fits in maxsize
        ti_files.showHeader(bytes)
        if not ti_files.isValid(bytes):
            raise Exception("not tifiles format")
        if not ti_files.isProgram(bytes):
            raise Exception("not PROGRAM image file")
        filesize = ti_files.byteLength(bytes)
        modeSend()
        sendByte(SUCCESS)
        print "sent SUCCESS, meaning ready to send stream"
        # Just cause DSR doesn't have a global SYN for reading.
	print "Length of file is: " + str(filesize)
        filesizemsb = (filesize & 0xFF00) >> 8
        print "set size msb: " + hex(filesizemsb)[2:].zfill(2)
        filesizelsb = (filesize & 0xFF)
        print "set size lsb: " + hex(filesizelsb)[2:].zfill(2)
        resetProtocol()
        modeSend()
        sendByte(filesizemsb)
        sendByte(filesizelsb)
	resetProtocol()
	modeSend()
        for byte in (bytes[128:])[:filesize]:
            sendByte(byte)
        print "finished sending all the bytes."
    except Exception as e:
        print e
        # I don't think this will work. we need to check for as many errors as possible up front.
	modeSend()
        sendErrorCode(EFILERR)
    finally:
        if fh != None:
            fh.close()
    
## 
## MAIN
##

# Initial device state.
setRD(0x00)
setRC(0x00)

for i in [ 1, 2, 4, 8, 16, 32, 64, 128, 64, 32, 16, 8, 4, 2, 1, 0 ]:
    setRD(i)
    time.sleep(0.05)

for i in [ 8, 4, 2, 1, 2, 4, 8, 0 ]:
    setRC(i)
    time.sleep(0.05)

while True:
    print "Ready for request..."
    resetProtocol()

    print "waiting for PAB..."
    modeRead()
    pab = bytearray(10)
    for i in range(0,10):
        pab[i] = readByte()
	print "PAB[" + str(i) + "]: " + hex(pab[i])[2:].zfill(2)

    print "PAB received."
    resetProtocol()

    modeRead()
    print "waiting for devicename..."
    devicename = bytearray(pab[9])
    for i in range(0,pab[9]):
        devicename[i] = readByte()
        print "devname[" + str(i) + "]: " + chr(devicename[i])

    # every path from here is a response back, so switching flags requires a reset in-between
    resetProtocol()

    # Special file name requests to force different errors
    filename = str(devicename)
    if filename == "TIPI.EDVNAME":
        sendErrorCode(EDVNAME)
    elif filename == "TIPI.EWPROT":
        sendErrorCode(EWPROT)
    elif filename == "TIPI.EOPATTR":
        sendErrorCode(EOPATTR)
    elif filename == "TIPI.EILLOP":
        sendErrorCode(EILLOP)
    elif filename == "TIPI.ENOSPAC":
        sendErrorCode(ENOSPAC)
    elif filename == "TIPI.EEOF":
        sendErrorCode(EEOF)
    elif filename == "TIPI.EDEVERR":
        sendErrorCode(EDEVERR)
    elif filename == "TIPI.EFILERR":
        sendErrorCode(EFILERR)
    else:
        switcher = {
            5: handleLoad
        }
        handler = switcher.get(opcode(pab), handleNotSupported)
        handler(pab, devicename)

    print "Request completed."


