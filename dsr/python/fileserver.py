#!/usr/bin/env python
import sys
import time
import RPi.GPIO as GPIO 
from array import array
import re
from ti_files import ti_files
from tipi import TipiMessage


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
    global tipi_io
    print "responding with error: " + str(code)
    msg = bytearray(1)
    msg[0] = code
    tipi_io.send(msg)

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
        sendErrorCode(SUCCESS)

        print "sent SUCCESS, meaning ready to send stream"
        # Just cause DSR doesn't have a global SYN for reading.
	print "Length of file is: " + str(filesize)
        filesizemsb = (filesize & 0xFF00) >> 8
        print "set size msb: " + hex(filesizemsb)[2:].zfill(2)
        filesizelsb = (filesize & 0xFF)
        print "set size lsb: " + hex(filesizelsb)[2:].zfill(2)

        tipi_io.send((bytes[128:])[:filesize])
        print "finished sending all the bytes."

    except Exception as e:
        print e
        # I don't think this will work. we need to check for as many errors as possible up front.
        sendErrorCode(EFILERR)
    finally:
        if fh != None:
            fh.close()
    
## 
## MAIN
##

tipi_io = TipiMessage()

while True:
    print "waiting for PAB..."

    pab = tipi_io.receive()

    print "PAB received."

    print "waiting for devicename..."
    devicename = tipi_io.receive()

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


