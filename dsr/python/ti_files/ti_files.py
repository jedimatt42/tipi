import os
import io
import sys
import traceback
import math
import logging

logger = logging.getLogger(__name__)


class ti_files(object):

    PROGRAM = 0x01
    INTERNAL = 0x02
    PROTECTED = 0x04
    VARIABLE = 0x08

    @staticmethod
    def isTiFile(filename):
        fh = None
        try:
            if os.stat(filename).st_size > 128:
                fh = open(filename, 'rb')
                header = bytearray(fh.read()[:9])
                isGood = ti_files.isValid(header)
                return isGood
        except Exception as e:
            logger.error(e, exc_info=True)
            pass
        finally:
            if fh is not None:
                fh.close()
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
    def isVariable(bytes):
        return ti_files.flags(bytes) & ti_files.VARIABLE

    @staticmethod
    def isValid(bytes):
        return bytes[0] == 0x07 and str(bytes[1:8]) == "TIFILES"

    @staticmethod
    def getSectors(bytes):
        return bytes[9] + (bytes[8] << 8)

    @staticmethod
    def flags(bytes):
        return bytes[10]

    @staticmethod
    def recordsPerSector(bytes):
        return bytes[11]

    @staticmethod
    def eofOffset(bytes):
        return bytes[12]

    @staticmethod
    def recordLength(bytes):
        return bytes[13]

    @staticmethod
    def recordCount(bytes):
        return bytes[15] + (bytes[14] << 8)

    @staticmethod
    def tiName(bytes):
        return str(bytes[0x10:0x1A])

    @staticmethod
    def byteLength(bytes):
        eofsize = ti_files.eofOffset(bytes)
        if eofsize == 0:
            eofsize = 256
        return ((ti_files.getSectors(bytes) - 1) * 256) + eofsize

    @staticmethod
    def dsrFileType(bytes):
        if ti_files.isProgram(bytes):
            return 5

        if ti_files.isInternal(bytes):
            if ti_files.isVariable(bytes):
                return 4
            else:
                return 3
        else:
            if ti_files.isVariable(bytes):
                return 2
            else:
                return 1

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

        if ti_files.isProtected(bytes):
            type += " Protected"

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
    def readRecord(bytes, recNumber):
        if ti_files.isVariable(bytes):
            return ti_files.readVariableRecord(bytes, recNumber)
        else:
            return ti_files.readFixedRecord(bytes, recNumber)

    @staticmethod
    def readVariableRecord(bytes, recNumber):
        logger.debug("read var record %d", recNumber)
        data = bytes[128:]
        sec = 0
        rIdx = 0
        offset = 0
        nextoff = offset + data[offset] + 1
        try:
            while rIdx < recNumber:
                offset = nextoff
                if data[offset] == 0xff:
                    # we need to move to the next sector
                    offset = int((offset / 256) + 1) * 256
                    nextoff = offset + data[offset] + 1
                else:
                    nextoff += data[offset] + 1
                rIdx += 1
            return bytearray(data[offset + 1:nextoff])
        except BaseException:
            return None

    @staticmethod
    def readFixedRecord(bytes, recNumber):
        reclen = ti_files.recordLength(bytes)
        maxRecNo = ti_files.byteLength(bytes) / reclen
        logger.debug("read fix record %d of %d", recNumber, maxRecNo)
        if recNumber > maxRecNo:
            return None
        data = bytes[128:]
        offset = reclen * recNumber
        try:
            return bytearray(data[offset:offset + reclen])
        except BaseException:
            return None

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
    def createProgramImage(devname, bytes, unix_name):
        nameParts = str(devname).split('.')
        tiname = nameParts[len(nameParts) - 1]

        header = ti_files.createHeader(ti_files.PROGRAM, tiname, bytes)
        fdata = bytearray(256 * (len(bytes) / 256 + 1) + 128)
        fdata[0:127] = header
        fdata[128:] = bytes
        return fdata
