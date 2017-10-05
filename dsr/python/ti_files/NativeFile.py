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

dv80suffixes = (".txt", ".a99", ".b99", ".bas", ".xb")

class NativeFile(object):

    def __init__(self, records, recordLength, statByte):
        self.records = records
        self.currentRecord = 0
        self.recordLength = recordLength
        self.statByte = statByte

    @staticmethod
    def load(unix_file_name, pab):
        try:
            if unix_file_name.lower().endswith(dv80suffixes):
                records = NativeFile.loadLines(unix_file_name)
                recLen = 80
                statByte = STVARIABLE
            else:
                records = NativeFile.loadBytes(unix_file_name)
                recLen = 128
                statByte = 0
                if dataType(pab):
                    statByte |= STINTERNAL
            return NativeFile(records, recLen, statByte)
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
                records += [bytearray(l.rstrip())]
        return records

    @staticmethod
    def loadBytes(fp):
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

    @staticmethod
    def status(fp):
        if fp.lower().endswith(dv80suffixes):
            statByte = STVARIABLE
        else:
            statByte = 0
        return statByte

    def isLegal(self, pab):
        return mode(pab) == INPUT

    def getStatusByte(self):
        statByte = self.statByte
        if self.currentRecord >= len(self.records):
            statByte |= STLEOF
        return statByte

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



