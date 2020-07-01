import os
import io
import sys
import traceback
import math
import logging
from . import ti_files
from Pab import *

logger = logging.getLogger(__name__)


class FixedRecordFile(object):
    def __init__(self, bytes, pab):
        self.dirty = False
        self.header = bytes[:128]
        self.mode = mode(pab)
        self.filetype = fileType(pab)
        self.recordLength = ti_files.recordLength(self.header)
        if self.mode == OUTPUT and self.filetype == SEQUENTIAL:
            self.records = []
            self.dirty = True
        else:
            self.records = self.__loadRecords(bytes[128:])
        if self.mode == APPEND:
            self.currentRecord = len(self.records)
        else:
            self.currentRecord = 0
        logger.info(
            "records loaded: %d, currentRecord: %d, recordLength: %d",
            len(self.records),
            self.currentRecord,
            self.recordLength,
        )

    @staticmethod
    def create(devname, localpath, pab):
        nameParts = str(devname).split(".")
        tiname = nameParts[len(nameParts) - 1]
        recLen = recordLength(pab)
        if recLen == 0:
            recLen = 80
        # FIXED is default (or flag clear/unset)
        flags = 0
        if dataType(pab) == INTERNAL:
            flags |= ti_files.INTERNAL
        header = ti_files.createHeader(flags, tiname, bytearray(0))
        ti_files.setRecordLength(header, recLen)
        ti_files.setRecordsPerSector(header, int(256 / recLen))
        recordFile = FixedRecordFile(header, pab)
        recordFile.dirty = True
        return recordFile

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
            return FixedRecordFile(fdata, pab)
        except Exception as e:
            logger.error("File does not match PAB type: %s", unix_file_name)
            return None
        finally:
            if fh != None:
                fh.close()

    def isLegal(self, pab):
        return recordType(pab) == FIXED

    def getStatusByte(self):
        statByte = 0
        if ti_files.isInternal(self.header):
            statByte |= STINTERNAL
        if self.currentRecord >= len(self.records):
            statByte |= STLEOF
        return statByte

    def restore(self, pab):
        logger.info("restore for file type: %d", self.filetype)
        if self.filetype == RELATIVE:
            self.currentRecord = recordNumber(pab)
        else:
            self.currentRecord = 0

    def writeRecord(self, rdata, pab):
        self.dirty = True
        recNo = recordNumber(pab)
        if self.filetype == RELATIVE:
            self.currentRecord = recNo
        if self.currentRecord >= len(self.records):
            logger.info("growing records")
            self.records += [bytearray(self.recordLength)] * (
                1 + self.currentRecord - len(self.records)
            )
        record = self.records[self.currentRecord]
        record[: len(rdata)] = bytearray(rdata)
        logger.info(
            "set record %d to bytes of length %d", self.currentRecord, len(rdata)
        )
        self.currentRecord += 1

    def readRecord(self, idx):
        if self.filetype == RELATIVE:
            self.currentRecord = idx
        logger.info("reading currentRecord: %d", self.currentRecord)
        record = self.getRecord(self.currentRecord)
        self.currentRecord += 1
        return record

    def getRecord(self, idx):
        if idx >= len(self.records):
            return None
        return self.records[idx]

    def getRecordLength(self):
        return self.recordLength

    def __loadRecords(self, bytes):
        count = ti_files.recordCount(self.header)
        idx = 0
        records = []

        while idx < count:
            record = self.__recordBytes(bytes, idx)
            if record == None:
                break
            records.append(record)
            idx += 1
        return records

    def __recordBytes(self, bytes, idx):
        recPerSec = int(256 / self.recordLength)
        secNumber = int(idx / recPerSec)
        recInSec = idx % recPerSec
        start = (secNumber * 256) + (recInSec * self.recordLength)
        end = start + self.recordLength
        return bytes[start:end]

    def close(self, localPath):
        if self.dirty:
            try:
                bytes = self.__packRecords()
                fh = open(localPath, "wb")
                fh.write(bytes)
                fh.close()
                self.dirty = False
            except Exception as e:
                logger.exception("Failed to save fixed file %s", localPath)

    def __packRecords(self):
        recLen = self.recordLength
        sectors = []
        sector = bytearray(256)
        recNo = 0
        offset = 0
        while recNo < len(self.records):
            rec = self.records[recNo]
            if (256 - offset) < (recLen):
                sectors += [sector]
                offset = 0
                sector = bytearray(256)
            sector[offset : offset + recLen] = rec
            offset += recLen
            recNo += 1

        if offset != 0:
            sectors += [sector]
        sectorCount = len(sectors)

        header = bytearray(self.header)
        ti_files.setSectors(header, sectorCount)
        if offset == 256:
            offset = 0
        ti_files.setEofOffset(header, offset)
        ti_files.setRecordCount(header, len(self.records))

        bytes = bytearray(128 + (sectorCount * 256))
        bytes[:128] = header
        idx = 128
        sec = 0
        while sec < sectorCount:
            bytes[idx:] = sectors[sec]
            sec += 1
            idx += 256
        return bytes
