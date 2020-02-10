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

dv80suffixes = (".cmd", ".txt", ".a99", ".b99", ".bas", ".xb")

class NativeFile(object):

    def __init__(self, records, recordLength, statByte,pab):
        self.records = records
        self.currentRecord = 0
        self.recordLength = recordLength
        self.statByte = statByte
        self.filetype = fileType(pab)

    @staticmethod
    def load(unix_file_name, pab, url=""):
        if mode(pab) != INPUT:
            raise Exception("Native files are read only")

        try:
            if recordType(pab) == VARIABLE and (unix_file_name.lower().endswith(dv80suffixes) or url.lower().endswith(dv80suffixes)):
                if recordLength(pab) != 80 and recordLength(pab) != 0:
                    raise Exception("Incompatible recordlength")
                logger.debug("using D/V 80 mode")
                records = NativeFile.loadLines(unix_file_name)
                logger.debug("loaded {} lines", len(records))
                recLen = 80
                statByte = STVARIABLE
            else:
                if recordLength(pab) != 128 and recordLength(pab) != 0:
                    raise Exception("Incompatible recordlength")
                logger.debug("using Fixed 128 mode")
                records = NativeFile.loadBytes(unix_file_name)
                logger.debug("loaded {} records", len(records))
                recLen = 128
                statByte = 0
                if dataType(pab):
                    statByte |= STINTERNAL
            return NativeFile(records, recLen, statByte, pab)

        except Exception as e:
            logger.exception("not a valid NativeFile %s", unix_file_name)
            raise

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
    def status(fp, url=""):
        if fp.lower().endswith(dv80suffixes) or url.lower().endswith(dv80suffixes):
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

    def restore(self, pab):
        if self.filetype == RELATIVE:
            self.currentRecord = recordNumber(pab)
        else:
            self.currentRecord = 0

    def readRecord(self, idx):
        if self.filetype == RELATIVE:
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

    def close(self, localPath):
        pass


