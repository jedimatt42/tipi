import os
import io
import sys
import traceback
import math
import logging
from ti_files import ti_files
from Pab import *

logger = logging.getLogger(__name__)

dv80suffixes = (".cmd", ".txt", ".a99", ".b99", ".bas", ".xb", ".tb")


class NativeFile(object):
    def __init__(self, records, recordLength, statByte, pab):
        self.records = records
        self.currentRecord = 0
        self.recordLength = recordLength
        self.statByte = statByte
        self.filetype = fileType(pab)

    @staticmethod
    def load(unix_file_name, pab, url=""):
        logger.info("loading as native file: %s", url)
        if mode(pab) != INPUT:
            raise Exception("Native files are read only")

        try:
            if recordType(pab) == VARIABLE:
                recLen = recordLength(pab)
                if recordLength(pab) == 0:
                    recLen = 80
                records = NativeFile.loadLines(unix_file_name, recLen)
                logger.info("loaded %d lines", len(records))
                logger.info("records: %s", records)
                statByte = STVARIABLE
            else:
                recLen = recordLength(pab)
                if recordLength(pab) == 0:
                    recLen = 128
                records = NativeFile.loadBytes(unix_file_name, recLen)
                logger.info("loaded %d records", len(records))
                logger.info("records: %s", records)
                statByte = 0
                if dataType(pab):
                    statByte |= STINTERNAL

            return NativeFile(records, recLen, statByte, pab)

        except Exception as e:
            logger.exception("not a valid NativeFile %s", unix_file_name)
            raise

    @staticmethod
    def loadLines(fp, recLen):
        i = 0
        records = []
        with open(fp) as f:
            for i, l in enumerate(f):
                bytes = bytearray(l.rstrip())
                if len(bytes) > 0:
                    records += NativeFile.divide_chunks(bytes, recLen)
                else:
                    records += [bytearray()]
        return records

    @staticmethod
    def loadBytes(fp, recLen):
        records = []
        with open(fp) as f:
            bytes = bytearray(f.read())
            records += NativeFile.divide_chunks(bytes, recLen, True)
        return records

    @staticmethod
    def divide_chunks(l, n, pad=False):
        for i in range(0, len(l), n):
            if pad:
                y = bytearray(n)
                s = l[i : i + n]
                y[0 : len(s)] = s
                yield y
            else:
                yield l[i : i + n]

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
