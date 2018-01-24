import os
import io
import sys
import traceback
import math
import logging
import uuid
import re
from subprocess import call

logger = logging.getLogger(__name__)


class ti_files(object):

    PROGRAM = 0x01
    INTERNAL = 0x02
    PROTECTED = 0x08
    VARIABLE = 0x80

    @staticmethod
    def isTiFile(filename):
        try:
            if os.path.exists(filename) and os.stat(filename).st_size >= 128:
                with open(filename, 'rb') as fh:
                    header = bytearray(fh.read())
                    isGood = ti_files.isValid(header)
                    return isGood
        except Exception as e:
            logger.error(e, exc_info=True)
            pass
        return False

    @staticmethod
    def isProgram(bytes):
        return ti_files.flags(bytes) & ti_files.PROGRAM

    @staticmethod
    def isInternal(bytes):
        return ti_files.flags(bytes) & ti_files.INTERNAL

    @staticmethod
    def isProtected(bytes):
        return ti_files.flags(bytes) & ti_files.PROTECTED

    @staticmethod
    def setProtected(bytes,value):
        if value != 0:
            bytes[10] = bytes[10] | ti_files.PROTECTED
        else:
            bytes[10] = bytes[10] ^ ti_files.PROTECTED

    @staticmethod
    def isVariable(bytes):
        return ti_files.flags(bytes) & ti_files.VARIABLE

    @staticmethod
    def isValid(bytes):
        return len(bytes) >= 128 and bytes[0] == 0x07 and str(bytes[1:8]) == "TIFILES"

    @staticmethod
    def setTiFile(bytes):
        bytes[0] = 0x07
        bytes[1:8] = "TIFILES"

    @staticmethod
    def getSectors(bytes):
        return bytes[9] + (bytes[8] << 8)

    @staticmethod
    def setSectors(bytes, sectors):
        lsb = 0xff & sectors
        msb = sectors >> 8
        bytes[8] = msb
        bytes[9] = lsb

    @staticmethod
    def flags(bytes):
        return bytes[10]

    @staticmethod
    def recordsPerSector(bytes):
        return bytes[11]

    @staticmethod
    def setRecordsPerSector(bytes, rps):
        bytes[11] = rps

    @staticmethod
    def eofOffset(bytes):
        return bytes[12]

    @staticmethod
    def setEofOffset(bytes, offset):
        bytes[12] = offset

    @staticmethod
    def recordLength(bytes):
        return bytes[13]

    @staticmethod
    def setRecordLength(bytes, recLen):
        bytes[13] = recLen

    @staticmethod
    def recordCount(bytes):
        return bytes[14] + (bytes[15] << 8)

    @staticmethod
    def setRecordCount(bytes, count):
        lsb = count & 0xff
        msb = count >> 8
        bytes[14] = lsb
        bytes[15] = msb

    @staticmethod
    def tiName(bytes):
        return str(bytes[0x10:0x1A])

    @staticmethod
    def setName(bytes, shortName):
        bytes[0x10:0x1A] = shortName

    @staticmethod
    def byteLength(bytes):
        eofsize = ti_files.eofOffset(bytes)
        if eofsize == 0:
            eofsize = 256
        return ((ti_files.getSectors(bytes) - 1) * 256) + eofsize

    @staticmethod
    def catFileType(bytes):
        protected = 1
	if ti_files.isProtected(bytes):
            protected = -1
        if ti_files.isProgram(bytes):
            return 5 * protected

        if ti_files.isInternal(bytes):
            if ti_files.isVariable(bytes):
                return 4 * protected
            else:
                return 3 * protected
        else:
            if ti_files.isVariable(bytes):
                return 2 * protected
            else:
                return 1 * protected

        return 0

    @staticmethod
    def flagsToString(bytes):
        if ti_files.isInternal(bytes):
            type = "INT/"
        else:
            type = "DIS/"
        if ti_files.isVariable(bytes):
            type += "VAR"
        else:
            type += "FIX"

        if ti_files.isProgram(bytes):
            type = "PROGRAM"

        return type

    @staticmethod
    def showHeader(bytes):
        if ti_files.isValid(bytes):
            logger.debug("TIFILES Header: ")
            logger.debug("  [8,9]  sectors: " +
                         str(ti_files.getSectors(bytes)))
            logger.debug("   [10]  type: " +
                         str(ti_files.flagsToString(bytes)))
            logger.debug("   [11]  records per sector: " +
                         str(ti_files.recordsPerSector(bytes)))
            logger.debug("   [12]  eofOffset: " +
                         str(ti_files.eofOffset(bytes)))
            logger.debug("   [13]  record length: " +
                         str(ti_files.recordLength(bytes)))
            logger.debug("[14,15]  record count: " +
                         str(ti_files.recordCount(bytes)))
            logger.debug("[16:26]  name: " + str(ti_files.tiName(bytes)))
        else:
            logger.error("not TIFILES header")

    @staticmethod
    def createHeader(flags, tiname, data):
        # create a 128 byte array, set flag byte,
        # copy in tiname
        # set record counts based on data array. (not sufficient)
        header = bytearray(128)
        header[0] = 0x07
        header[1:7] = bytearray("TIFILES")
        header[10] = flags

        datalen = len(data)
        sectors = datalen / 256
        eofOffset = datalen % 256
        if eofOffset != 0:
            sectors += 1
        header[8] = sectors >> 8
        header[9] = sectors & 0xFF
        header[12] = eofOffset

        header[0x10:0x1A] = bytearray(tiname)
        return header

    @staticmethod
    def validateDataType(fdata, dataType):
        if dataType != 0 and ti_files.isInternal(fdata) != 0:
            return
        if dataType == 0 and ti_files.isInternal(fdata) == 0:
            return
        raise Exception("mismatch data type")

    @staticmethod
    def isTiBasicAscii(filename):   # Returns true if file is detected to be an ASCII BASIC program.
        with open(filename, 'r') as f:
            line = f.readline()

        if re.match(r"^\d+\s(\w+|\!)", line) is not None:
            return True
        return False

    @staticmethod
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
                    if not ti_files.isProgram(bytes):
                        return False
                    program.write(bytes[128:])

            call(['/home/tipi/xdt99/xbas99.py', '-d', prg_tmp_file, '-o', bas_tmp_file])         

            return ti_files.isTiBasicAscii(bas_tmp_file)

        except Exception as e:
            return False

        finally:
            if os.path.exists(prg_tmp_file):
                os.unlink(prg_tmp_file)
            if os.path.exists(bas_tmp_file):
                os.unlink(bas_tmp_file)

        return False

