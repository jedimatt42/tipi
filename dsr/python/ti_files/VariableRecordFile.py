import os
import io
import sys
import traceback
import math
import logging
from ti_files import ti_files
from Pab import *

logger = logging.getLogger(__name__)

class VariableRecordFile(object):

    def __init__(self, bytes):
        self.header = bytes[:128]
        self.recordLength = ti_files.recordLength(self.header)
        self.records = self.__loadRecords(bytes[128:])
        self.currentRecord = 0

    @staticmethod
    def load(unix_file_name, dataType):
        fh = None
        try:
            fh = open(unix_file_name, "rb")
            fdata = bytearray(fh.read())
            # Check that request matches DISPLAY or INTERNAL of file
            ti_files.validateDataType(fdata, dataType)

            # Check that target file is valid
            if not ti_files.isValid(fdata):
                raise Exception("invalid TIFILE")
            # Check that we are a VARIABLE record file
            logger.debug("flags %d", ti_files.flags(fdata))
            if not ti_files.isVariable(fdata):
                raise Exception("file is FIXED, must be VARIABLE")
            return VariableRecordFile(fdata)
        except Exception as e:
            traceback.print_exc()
            logger.error("not a valid Variable Record TIFILE %s", unix_file_name)
            return None
        finally:
            if fh != None:
                fh.close()

    def __loadRecords(self, bytes):
        count = ti_files.recordCount(bytes)
        idx = 0
        records = []
        while idx < count:
            # Todo: migrate readFixedRecord code into this class
            record = self.__readVariableRecord(bytes, idx)
            if record == None:
                break
            records.append(record)
            idx += 1
        return records

    def isLegal(self, pab):
        return mode(pab) == INPUT and recordType(pab) != FIXED

    def readRecord(self, idx):
        if idx != 0:
            self.currentRecord = idx
        record = self.getRecord(self.currentRecord)
        self.currentRecord += 1
        return record

    def getRecord(self, idx):
        if idx >= len(self.records):
            return None
        return self.records[idx]

    def getRecordLength(self):
        return self.recordLength

    def __readVariableRecord(self, bytes, idx):
        logger.debug("read var record %d", idx)
        sec = 0
        rIdx = 0
        offset = 0
        nextoff = offset + bytes[offset] + 1
        try:
            while rIdx < idx:
                offset = nextoff
                if bytes[offset] == 0xff:
                    # we need to move to the next ~sector~
                    offset = int((offset / 256) + 1) * 256
                    nextoff = offset + bytes[offset] + 1
                else:
                    nextoff += bytes[offset] + 1
                rIdx += 1
            return bytearray(bytes[offset + 1:nextoff])
        except BaseException:
            return None