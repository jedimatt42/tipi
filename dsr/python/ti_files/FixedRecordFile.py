import os
import io
import sys
import traceback
import math
import logging
from ti_files import ti_files

logger = logging.getLogger(__name__)

class FixedRecordFile(ti_files):

    def __init__(self, bytes):
        self.header = bytes[:128]
        self.recordSize = self.recordLength(header)
        self.records = self.__loadRecords(bytes)

    @staticmethod
    def load(unix_file_name):
        fh = None
        try:
            fh = fopen(unix_file_name, "rb")
            bytes = fh.read()
            if ti_files.isValid(bytes) and !ti_files.isVariable(bytes):
                return FixedRecordFile(bytes)
        except expression as identifier:
            logger.error("not a valid Fixed Record TIFILE %s", unix_file_name)
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
            records[idx] = ti_files.readFixedRecord(idx)
            idx += 1
        return records

    def getRecord(self, idx):
        return self.records[idx]
