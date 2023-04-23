import logging
from TipiConfig import TipiConfig
from Pab import *

logger = logging.getLogger(__name__)

tipi_config = TipiConfig.instance()

class ForthFile(object):
    def __init__(self, unix_file_name, statByte, pab):
        self.recordLength = 128
        self.statByte = statByte
        self.pab = pab
        self.filetype = fileType(pab)
        self.loadRecords(unix_file_name)

    @staticmethod
    def load(unix_file_name, pab, native_flags):
        logger.info("creating as Forth file")
        if recordType(pab) == VARIABLE:
            return None
        recLen = recordLength(pab)
        if recLen != 0 and recLen != 128:
            return None

        statByte = 0
        if dataType(pab):
            statByte |= STINTERNAL
        return ForthFile(unix_file_name, statByte, pab)

    # query the data structure and set records based on result string
    def loadRecords(self, unix_file_name):
        self.records = []
        self.currentRecord = 0

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
        pass

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

    def close(self, unix_file_name):
        pass

    def eager_write(self, unix_file_name):
        self.close(unix_file_name)

