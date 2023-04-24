import logging
from .JsonFile import JsonFile
from .ForthFile import ForthFile
from tinames.tinames import JSON_NATIVE
from TipiConfig import TipiConfig
from Pab import *

logger = logging.getLogger(__name__)

dv80suffixes = (".cmd", ".txt", ".a99", ".b99", ".bas", ".xb", ".tb")

tipi_config = TipiConfig.instance()

class NativeFile(object):
    def __init__(self, records, recordLength, statByte, pab, native_flags):
        self.dirty = False
        self.records = records
        self.currentRecord = 0
        self.recordLength = recordLength
        self.statByte = statByte
        self.filetype = fileType(pab)
        self.pab = pab
        self.native_flags = native_flags
        if self.native_flags == "?W":
            host_eol = tipi_config.get("HOST_EOL", '\r\n')
            # bad input / safe default
            self.line_ending = '\r\n'
            if host_eol == "CRLF":
                self.line_ending = '\r\n'
            elif host_eol == "LF":
                self.line_ending = '\n'
        else:
            self.line_ending = ''


    @staticmethod
    def load(unix_file_name, pab, native_flags, url=""):
        logger.info("loading as native file: %s", url)

        if JSON_NATIVE in native_flags:
            return JsonFile.load(unix_file_name, pab, native_flags)

        if unix_file_name.lower().endswith(".fb"):
            return ForthFile.load(unix_file_name, pab)

        if mode(pab) == OUTPUT:
            return NativeFile.create(unix_file_name, pab, native_flags)

        try:
            if recordType(pab) == VARIABLE:
                recLen = recordLength(pab)
                if recordLength(pab) == 0:
                    recLen = 80
                encoding = 'utf-8' if url else 'latin1'
                records = NativeFile.loadLines(unix_file_name, recLen, encoding)
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

            nf = NativeFile(records, recLen, statByte, pab, native_flags)
            if mode(pab) == APPEND:
                nf.currentRecord = len(records)
            return nf

        except Exception:
            logger.exception("not a valid NativeFile %s", unix_file_name)
            raise

    @staticmethod
    def create(unix_file_name, pab, native_flags):
        logger.info("creating as native file")
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
        return NativeFile([], recLen, statByte, pab, native_flags)

    @staticmethod
    def loadLines(unix_file_name, recLen, encoding='latin1'):
        i = 0
        records = []
        with open(unix_file_name, 'r', encoding=encoding) as f:
            for i, l in enumerate(f):
                bytes = bytearray(l.rstrip(), encoding)
                if len(bytes) > 0:
                    records += NativeFile.divide_chunks(bytes, recLen)
                else:
                    records += [bytearray()]
        return records

    @staticmethod
    def loadBytes(unix_file_name, recLen):
        records = []
        with open(unix_file_name, 'rb') as f:
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

    def writeRecord(self, rdata, pab):
        self.dirty = True
        if self.currentRecord >= len(self.records):
            self.records += [bytearray(0)] * (
                1 + self.currentRecord - len(self.records)
            )
        self.records[self.currentRecord] = bytearray(rdata)
        self.currentRecord += 1

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
        if self.dirty:
            try:
                if self.native_flags == "?W":
                    if dataType(self.pab) == DISPLAY:
                        self.writeLines(localPath)
                    else:
                        raise Exception("only DISPLAY format supported")
                    self.dirty = False
                elif self.native_flags == "?X":
                    self.writeBinary(localPath)

            except Exception as e:
                logger.exception("Failed to save file %s", localPath)
                raise e

    def eager_write(self, localPath):
        self.close(localPath)

    def writeLines(self, localPath):
        with open(localPath, "w") as fh:
            fh.writelines(str(line, 'latin1') + self.line_ending for line in self.records)

    def writeBinary(self, localPath):
        with open(localPath, "wb") as fh:
            for record in self.records:
                fh.write(record)

