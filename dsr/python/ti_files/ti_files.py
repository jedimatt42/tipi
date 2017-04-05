import os
import sys
import traceback
import math

class ti_files(object):

    @staticmethod
    def isTiFile(filename):
        fh = None
        try:
            if os.stat(filename).st_size > 128:
                fh = open(filename,'rb')
                header = bytearray(fh.read()[:9])
                isGood = ti_files.isValid(header)
                return isGood
        except Exception as e:
            traceback.print_exc()
            pass
        finally:
            if fh != None:
                fh.close()
        return False

    @staticmethod
    def isProgram(bytes):
        return ti_files.flags(bytes) & 0x01

    @staticmethod
    def isInternal(bytes):
        return ti_files.flags(bytes) & 0x02

    @staticmethod
    def isProtected(bytes):
        return ti_files.flags(bytes) & 0x04

    @staticmethod
    def isVariable(bytes):
        return ti_files.flags(bytes) & 0x80

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
        return ((ti_files.getSectors(bytes)-1) * 256) + eofsize

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
        print "TIFILES Header: "
        print "  name: " + str(ti_files.tiName(bytes))
        print "  type: " + str(ti_files.flagsToString(bytes))
        print "  sectors: " + str(ti_files.getSectors(bytes))
        print "  records: " + str(ti_files.recordsPerSector(bytes))
        print "  eof: " + str(ti_files.eofOffset(bytes))
        print "  record length: " + str(ti_files.recordLength(bytes))
        print "  record count: " + str(ti_files.recordCount(bytes))

    @staticmethod
    def readRecord(bytes, recNumber):
        if ti_files.isVariable(bytes):
            return ti_files.readVariableRecord(bytes, recNumber)
        else:
            return ti_files.readFixedRecord(bytes, recNumber)

    @staticmethod
    def readVariableRecord(bytes, recNumber):
        print "read var record {}".format(recNumber)
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
	    return bytearray(data[offset+1:nextoff])
        except:
            return None
        
    @staticmethod
    def readFixedRecord(bytes, recNumber):
        print "read fix record {}".format(recNumber)
        data = bytes[128:]
        reclen = ti_files.recordLength(bytes)
        offset = reclen * recNumber
        try:
            return bytearray(data[offset:offset+reclen])
        except:
            return None


