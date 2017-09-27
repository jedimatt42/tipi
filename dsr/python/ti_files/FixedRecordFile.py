import os
import io
import sys
import traceback
import math
import logging
from ti_files import ti_files
from Pab import *

logger = logging.getLogger(__name__)

class FixedRecordFile(object):

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
                raise Exception("invaid TIFILE")
            # Check that we are a FIXED record file
            if ti_files.isVariable(fdata):
                raise Exception("file is variable")
            return FixedRecordFile(fdata)
        except Exception as e:
            traceback.print_exc()
            logger.error("not a valid Fixed Record TIFILE %s", unix_file_name)
            return None
        finally:
            if fh != None:
                fh.close()

    def __loadRecords(self, bytes):
        count = ti_files.recordCount(self.header)
        idx = 0
        records = []
        while idx < count:
            # Todo: migrate readFixedRecord code into this class
            record = self.readFixedRecord(bytes, idx)
            if record == None:
                break
            records.append(record)
            idx += 1
        return records

    def isLegal(self, pab):
        return mode(pab) == INPUT and recordType(pab) == FIXED

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

    def readFixedRecord(self, bytes, idx):
        maxRecNo = ti_files.byteLength(self.header) / self.recordLength
        logger.debug("read fix record %d of %d", idx, maxRecNo)
        if idx > maxRecNo:
            return None
        offset = self.recordLength * idx
        try:
            return bytearray(bytes[offset:offset + self.recordLength])
        except BaseException:
            traceback.print_exc()
            return None

