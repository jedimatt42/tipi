#!/usr/bin/env python
import sys
import time
import RPi.GPIO as GPIO 
from array import array
import re
from ti_files import ti_files
from tipi.TipiMessage import TipiMessage

#
# Utils
#

def hexdump(bytes):
    for byte in bytes:
        print "{0:x}".format(byte),

#
# PAB routines...
#

#
# Return the TI DSR Opcode
def opcode(pab):
    return int(pab[0])

# Constants for fileType
SEQUENTIAL = 0x00
RELATIVE = 0x01

def fileType(pab):
    return (pab[1] & 0x01) 

# Constants for modes
UPDATE = 0x00
OUTPUT = 0x01
INPUT = 0x02
APPEND = 0x03

def mode(pab):
    return (pab[1] & 0x06) >> 1

# Data types
DISPLAY = 0x00
INTERNAL = 0x01

def dataType(pab):
    return (pab[1] & 0x08) >> 3

# Record types
FIXED = 0x00
VARIABLE = 0x01

def recordType(pab):
    return (pab[1] & 0x10) >> 4

# Length of file records
def recordLength(pab):
    return pab[4]

#
# Return byte count from PAB / or byte count in LOAD/SAVE operations
def recordNumber(pab):
    return (pab[6] << 8) + pab[7];

#
# pretty pab string
def printPab(pab):
    opcodes = { 0 : "Open", 1 : "Close", 2 : "Read", 3 : "Write", 4 : "Restore", 5 : "Load", 6 : "Save", 7 : "Delete", 8 : "Scratch", 9 : "Status" }
    fileTypes = { SEQUENTIAL : "Sequential", RELATIVE : "Relative" }
    modes = { UPDATE : "Update", OUTPUT : "Output", INPUT : "Input", APPEND : "Append" }
    dataTypes = { DISPLAY : "Display", INTERNAL : "Internal" }
    recordTypes = { FIXED : "Fixed", VARIABLE : "Variable" }
    print "opcode: {}, fileType: {}, mode: {}, dataType: {}, recordType: {}, recordLength: {}, recordNumber: {}".format(
      opcodes[opcode(pab)], 
      fileTypes[fileType(pab)], 
      modes[mode(pab)], 
      dataTypes[dataType(pab)], 
      recordTypes[recordType(pab)], 
      recordLength(pab), 
      recordNumber(pab) 
    )

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

def handleOpen(pab, devname):
    print "Opcode 0 Open - " + str(devname)
    printPab(pab)
    sendErrorCode(EDEVERR)

def handleClose(pab, devname):
    print "Opcode 1 Close - " + str(devname)
    printPab(pab)
    sendErrorCode(EDEVERR)

def handleRead(pab, devname):
    print "Opcode 2 Read - " + str(devname)
    printPab(pab)
    sendErrorCode(EDEVERR)

def handleWrite(pab, devname):
    print "Opcode 3 Write - " + str(devname)
    printPab(pab)
    sendErrorCode(EDEVERR)

def handleRestore(pab, devname):
    print "Opcode 4 Restore - " + str(devname)
    printPab(pab)
    sendErrorCode(EDEVERR)

def handleLoad(pab, devname):
    print "Opcode 5 LOAD - " + str(devname)
    printPab(pab)
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
    
def handleSave(pab, devname):
    print "Opcode 6 Save - " + str(devname)
    printPab(pab)
    sendErrorCode(EDEVERR)

def handleDelete(pab, devname):
    print "Opcode 7 Delete - " + str(devname)
    printPab(pab)
    sendErrorCode(EDEVERR)

def handleScratch(pab, devname):
    print "Opcode 8 Scratch - " + str(devname)
    printPab(pab)
    sendErrorCode(EDEVERR)

def handleStatus(pab, devname):
    print "Opcode 9 Status - " + str(devname)
    printPab(pab)
    sendErrorCode(EDEVERR)

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
            0: handleOpen,
            1: handleClose,
            2: handleRead,
            3: handleWrite,
            4: handleRestore,
            5: handleLoad,
            6: handleSave,
            7: handleDelete,
            8: handleScratch,
            9: handleStatus
        }
        handler = switcher.get(opcode(pab), handleNotSupported)
        handler(pab, devicename)

    print "Request completed."


