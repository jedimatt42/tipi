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
    def load(unix_file_name, pab):
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

    def loadRecords(self, unix_file_name):
        self.blocks = []
        self.blocks.append(bytearray(''.ljust(1024,' '),'ascii'))
        self.currentRecord = 0
        # read all the text, and pack it into Forth blocks
        #   if the text exceeds a block before the end of 
        #   the current block, add a '-->' next block command
        #   and continue packing into the next block
        cur_blk = 0
        i = 0
        with open(unix_file_name, "r") as f:
            lines = f.readlines()
            for l in lines:
                l = l.strip()
                l = ' '.join(l.split())
                logger.info("line: '%s'", l)
                llen = len(l)
                if i+llen+5 > 1023:
                   self.blocks[cur_blk][i+1:i+4] = bytearray("-->", 'ascii') 
                   cur_blk += 1
                   i = 0
                   self.blocks.append(bytearray(''.ljust(1024,' '),'ascii'))
                leading_space = 1 if i > 0 else 0
                self.blocks[cur_blk][i+leading_space:llen] = bytearray(l, 'ascii')
                i += llen + leading_space

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
        byte_idx = idx * 128
        if byte_idx > len(self.blocks) * 1024:
            return None
        bl_idx = byte_idx // 1024
        ibl_idx = byte_idx % 1024
        ebl_idx = ibl_idx + 128
        return self.blocks[bl_idx][ibl_idx:ebl_idx]

    def getRecordLength(self):
        return self.recordLength

    def close(self, unix_file_name):
        pass

    def eager_write(self, unix_file_name):
        self.close(unix_file_name)

