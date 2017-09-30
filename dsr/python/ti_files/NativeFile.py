import os
import io
import sys
import traceback
import math
import magic
import logging
from ti_files import ti_files
from Pab import *

logger = logging.getLogger(__name__)

dv80suffixes = (".txt", ".bas", ".xb", ".md")

class NativeFile(object):

    def __init__(self, records, recordLength):
        self.records = records
        self.currentRecord = 0
        self.recordLength = recordLength

    @staticmethod
    def load(unix_file_name, pab):
        try:
            if unix_file_name.lower().endswith(dv80suffixes):
                records = NativeFile.loadLines(unix_file_name)
                recLen = 80
            else:
                records = NativeFile.loadBytes(unix_file_name)
                recLen = 128
            return NativeFile(records, recLen)
        except Exception as e:
            traceback.print_exc()
            logger.error("not a valid Fixed Record TIFILE %s", unix_file_name)
            return None

    @staticmethod
    def loadLines(fp):
        i = 0
        records = []
        with open(fp) as f:
            for i, l in enumerate(f):
                records += [bytearray(l)]
        return records

    @staticmethod
    def loadBytes(fh):
        records = []
        with open(fp) as f:
            bytes = bytearray(f.read())
            while len(bytes) >= 128:
                records += [bytes[:128]]
                bytes = bytes[128:]
            if len(bytes) > 0:
                padded = bytearray(128)
                padded[0:] = bytes
                records += [padded]
        return records

    def isLegal(self, pab):
        return mode(pab) == INPUT

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



