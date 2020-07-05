import os
import io
import sys
import traceback
import math
import logging

logger = logging.getLogger(__name__)


PROGRAM = 0x01
INTERNAL = 0x02
PROTECTED = 0x08
VARIABLE = 0x80


def isTiFile(filename):
    fh = None
    try:
        if os.path.exists(filename) and os.stat(filename).st_size >= 128:
            fh = open(filename, 'rb')
            header = bytearray(fh.read()[:9])
            return isValid(header)
    except Exception as e:
        logger.error(e, exc_info=True)
        pass
    finally:
        if fh is not None:
            fh.close()
    return False

def get_file_type(filename):
    fh = None
    try:
        if os.path.exists(filename) and os.stat(filename).st_size >= 128:
            fh = open(filename, 'rb')
            header = bytearray(fh.read()[:128])
            isGood = isValid(header)
            if isGood:
                return shortFileType(header)
    except Exception as e:
        logger.error(e, exc_info=True)
        pass
    finally:
        if fh is not None:
            fh.close()
    return "native"


def isProgram(bytes):
    return flags(bytes) & PROGRAM


def isInternal(bytes):
    return flags(bytes) & INTERNAL


def isProtected(bytes):
    return flags(bytes) & PROTECTED


def setProtected(bytes,value):
    if value != 0:
        bytes[10] = bytes[10] | PROTECTED
    else:
        bytes[10] = bytes[10] ^ PROTECTED


def isVariable(bytes):
    return flags(bytes) & VARIABLE


def isValid(bytes):
    return bytes[0] == 0x07 and str(bytes[1:8], 'ascii') == "TIFILES"


def setTiFile(bytes):
    bytes[0] = 0x07
    bytes[1:8] = bytearray("TIFILES", 'ascii')


def getSectors(bytes):
    return bytes[9] + (bytes[8] << 8)


def setSectors(bytes, sectors):
    lsb = 0xff & sectors
    msb = sectors >> 8
    bytes[8] = msb
    bytes[9] = lsb


def flags(bytes):
    return bytes[10]


def recordsPerSector(bytes):
    return bytes[11]


def setRecordsPerSector(bytes, rps):
    bytes[11] = rps


def eofOffset(bytes):
    return bytes[12]


def setEofOffset(bytes, offset):
    bytes[12] = offset


def recordLength(bytes):
    return bytes[13]


def setRecordLength(bytes, recLen):
    bytes[13] = recLen


def recordCount(bytes):
    return bytes[14] + (bytes[15] << 8)


def setRecordCount(bytes, count):
    lsb = count & 0xff
    msb = count >> 8
    bytes[14] = lsb
    bytes[15] = msb


def tiName(bytes):
    return str(bytes[0x10:0x1A], 'ascii')


def setName(bytes, shortName):
    bytes[0x10:0x1A] = shortName


def byteLength(bytes):
    eofsize = eofOffset(bytes)
    if eofsize == 0:
        eofsize = 256
    return ((getSectors(bytes) - 1) * 256) + eofsize


def catFileType(bytes):
    protected = 1
    if isProtected(bytes):
        protected = -1
    if isProgram(bytes):
        return 5 * protected

    if isInternal(bytes):
        if isVariable(bytes):
            return 4 * protected
        else:
            return 3 * protected
    else:
        if isVariable(bytes):
            return 2 * protected
        else:
            return 1 * protected

    return 0


def shortFileType(bytes):
    if isInternal(bytes):
        type = "I"
    else:
        type = "D"
    if isVariable(bytes):
        type += "V"
    else:
        type += "F"

    if isProgram(bytes):
        type = "PRG"

    return type


def flagsToString(bytes):
    if isInternal(bytes):
        type = "INT/"
    else:
        type = "DIS/"
    if isVariable(bytes):
        type += "VAR"
    else:
        type += "FIX"

    if isProgram(bytes):
        type = "PROGRAM"

    if isProtected(bytes):
        type += " Protected"

    return type


def showHeader(bytes):
    if isValid(bytes):
        logger.debug("TIFILES Header: ")
        logger.debug("  [8,9]  sectors: " +
                     str(getSectors(bytes), 'ascii'))
        logger.debug("   [10]  type: " +
                     flagsToString(bytes))
        logger.debug("   [11]  records per sector: " +
                     recordsPerSector(bytes))
        logger.debug("   [12]  eofOffset: " +
                     eofOffset(bytes))
        logger.debug("   [13]  record length: " +
                     recordLength(bytes))
        logger.debug("[14,15]  record count: " +
                     recordCount(bytes))
        logger.debug("[16:26]  name: " + tiName(bytes))
    else:
        logger.error("not TIFILES header")


def createHeader(flags, tiname, data):
    # create a 128 byte array, set flag byte,
    # copy in tiname
    # set record counts based on data array. (not sufficient)
    header = bytearray(128)
    header[0] = 0x07
    header[1:8] = bytearray("TIFILES", 'ascii')
    header[10] = flags

    datalen = len(data)
    sectors = int(datalen / 256)
    eofOffset = int(datalen % 256)
    if eofOffset != 0:
        sectors += 1
    header[8] = sectors >> 8
    header[9] = sectors & 0xFF
    header[12] = eofOffset

    header[0x10:0x1A] = bytearray(tiname.ljust(10,' '), 'ascii')
    return header


def validateDataType(fdata, dataType):
    if dataType != 0 and isInternal(fdata) != 0:
        return
    if dataType == 0 and isInternal(fdata) == 0:
        return
    raise Exception("mismatch data type")
