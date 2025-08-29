import os
import io
import sys
import traceback
import math
import logging
import uuid
import re
from subprocess import call, DEVNULL

logger = logging.getLogger(__name__)



PROGRAM = 0x01
INTERNAL = 0x02
PROTECTED = 0x08
VARIABLE = 0x80

def isTiFile(filename):
    try:
        if os.path.exists(filename) and os.stat(filename).st_size >= 128:
            with open(filename, 'rb') as fh:
                header = bytearray(fh.read())
                isGood = isValid(header)
                return isGood
    except Exception as e:
        logger.error(e, exc_info=True)
        pass
    return False


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
    return len(bytes) >= 128 and bytes[0] == 0x07 and str(bytes[1:8], 'ascii') == "TIFILES"


def setTiFile(bytes):
    bytes[0] = 0x07
    bytes[1:8] = "TIFILES"


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

    return type


def showHeader(bytes):
    if isValid(bytes):
        logger.debug("TIFILES Header: ")
        logger.debug(f"  [8,9]  sectors: {getSectors(bytes)}")
        logger.debug(f"   [10]  type: {flagsToString(bytes)}")
        logger.debug(f"   [11]  records per sector: {recordsPerSector(bytes)}")
        logger.debug(f"   [12]  eofOffset: {eofOffset(bytes)}")
        logger.debug(f"   [13]  record length: {recordLength(bytes)}")
        logger.debug(f"[14,15]  record count: {recordCount(bytes)}")
        logger.debug(f"[16:26]  name: {str(tiName(bytes), 'ascii')}")
    else:
        logger.error("not TIFILES header")


def createHeader(flags, tiname, data):
    # create a 128 byte array, set flag byte,
    # copy in tiname
    # set record counts based on data array. (not sufficient)
    header = bytearray(128)
    header[0] = 0x07
    header[1:7] = bytearray("TIFILES", 'ascii')
    header[10] = flags

    datalen = len(data)
    sectors = datalen / 256
    eofOffset = datalen % 256
    if eofOffset != 0:
        sectors += 1
    header[8] = sectors >> 8
    header[9] = sectors & 0xFF
    header[12] = eofOffset

    header[0x10:0x1A] = bytearray(tiname, 'ascii')
    return header


def validateDataType(fdata, dataType):
    if dataType != 0 and isInternal(fdata) != 0:
        return
    if dataType == 0 and isInternal(fdata) == 0:
        return
    raise Exception("mismatch data type")


def isTiBasicAscii(filename):   # Returns true if file is detected to be an ASCII BASIC program.
    with open(filename, 'r') as f:
        line = f.readline()

    if re.match(r"^\d+\s(\w+|\!)", line) is not None:
        return True
    return False


def isTiBasicPrg(filename):     # Returns true if file is a PRG file and is detected to be BASIC.
    logger.debug("testing for is TIFILES BASIC PROGRAM in %s", filename)
    # We are assuming the test for FIAD isTiFile has already passed.

    prg_tmp_file = '/tmp/' + str(uuid.uuid4()) + '.tmp'
    bas_tmp_file = '/tmp/' + str(uuid.uuid4()) + '.tmp'

    try:
        # strip the FIAD header off to get the raw file xbas99 needs.
        with open(filename, "rb") as tifile:
            with open(prg_tmp_file, "wb") as program:
                bytes = bytearray(tifile.read())
                if isProgram(bytes):
                    program.write(bytes[128:])
                elif (isInternal(bytes) and isVariable(bytes) and (recordLength(bytes) == 254)):
                    ## internal file needs to be extracted differently but it has a marker... so we can cheat here.
                    return bytes[129:131] == "\xab\xcd" 
                else:
                    return False

        call(['/home/tipi/xdt99/xbas99.py', '-d', prg_tmp_file, '-o', bas_tmp_file],
                stdout=DEVNULL, stderr=DEVNULL)         

        return isTiBasicAscii(bas_tmp_file)

    except Exception as e:
        return False

    finally:
        if os.path.exists(prg_tmp_file):
            os.unlink(prg_tmp_file)
        if os.path.exists(bas_tmp_file):
            os.unlink(bas_tmp_file)

    return False

