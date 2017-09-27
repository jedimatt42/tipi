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
    def load(unix_file_name, pab):
        fh = None
        try:
            fh = open(unix_file_name, "rb")
            fdata = bytearray(fh.read())
            # Check that request matches DISPLAY or INTERNAL of file
            ti_files.validateDataType(fdata, dataType(pab))

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

    def __loadRecords(self, bytes):
        records = []
        # variable records return sectors instead of actual record count
        sectors = ti_files.recordCount(self.header)
        sIdx = 0
        offset = 0
        if len(bytes) <= offset:
            return records

        nextoff = offset + bytes[offset] + 1
        record = bytearray(bytes[offset + 1:nextoff])
        logger.debug("record: %s", str(record))
        records += [record]

        while sIdx < sectors:
            logger.debug("record %d of %d", sIdx, sectors)
            offset = nextoff
            if bytes[offset] == 0xff:
                sIdx += 1
                if sIdx >= sectors:
                    break
                # we need to move to the next ~sector~
                offset = int((offset / 256) + 1) * 256
                nextoff = offset + bytes[offset] + 1
            else:
                nextoff += bytes[offset] + 1
            record = bytearray(bytes[offset + 1:nextoff])
            logger.debug("record: %s", str(record))
            records += [record]
        return records