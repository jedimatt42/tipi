import os
import io
import sys
import traceback
import math
import logging
import json
import jmespath
from . import ti_files
from . import JsonFile
from TipiConfig import TipiConfig
from Pab import *

logger = logging.getLogger(__name__)

tipi_config = TipiConfig.instance()

class JsonFile(object):
    def __init__(self, pyData, records, recordLength, statByte, pab):
        self.pyData = pyData
        self.recordLength = recordLength
        self.statByte = statByte
        self.filetype = fileType(pab)
        self.pab = pab
        self.loadRecords("")

    @staticmethod
    def load(unix_file_name, pab, native_flags):
        logger.info("creating as json file")
        if recordType(pab) == VARIABLE:
            recLen = recordLength(pab)
            if recordLength(pab) == 0:
                recLen = 80
            statByte = STVARIABLE
        else:
            recLen = recordLength(pab)
            if recordLength(pab) == 0:
                recLen = 128
            statByte = 0
            if dataType(pab):
                statByte |= STINTERNAL
        with open(unix_file_name, "r") as f:
            pyData = json.load(f)
            return JsonFile(pyData, [], recLen, statByte, pab)

    # query the data structure and set records based on result string
    def loadRecords(self, expression):
        logger.info("jmespath expression: " + expression)
        if expression:
            try:
                result = jmespath.search(expression, self.pyData)
            except jmespath.exceptions.ParseError as e:
                result = str(e)
        else:
            # if no query expression is provided, return the entire data structure
            result = self.pyData
        # if we just have a sting left, then unquote it.
        if isinstance(result, str):
            resultStr = result
        else:
            resultStr = json.dumps(result, separators=(',',':'), sort_keys=True)
        logger.info("resultStr: " + resultStr)
        if recordType(self.pab) == VARIABLE:
            self.records = JsonFile.loadLines(resultStr, self.recordLength)
        else:
            self.records = JsonFile.loadBytes(resultStr, self.recordLength)
        self.currentRecord = 0

    @staticmethod
    def loadLines(jsonStr, recLen, encoding='latin1'):
        i = 0
        records = []

        bytes = bytearray(jsonStr.rstrip(), encoding)
        if len(bytes) > 0:
            records += JsonFile.divide_chunks(bytes, recLen)
        else:
            records += [bytearray()]
        return records

    @staticmethod
    def loadBytes(jsonStr, recLen):
        records = []
        records += JsonFile.divide_chunks(jsonStr, recLen, True)
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
        return True

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

    def writeRecord(self, rdata, pab):
        query = str(rdata, 'latin1')
        self.loadRecords(query)

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

    def eager_write(self, localPath):
        self.close(localPath)

