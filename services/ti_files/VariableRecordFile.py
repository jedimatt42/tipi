import os
import io
import sys
import math
import logging
from . import ti_files
from tinames import tinames
from tinames import NativeFlags
from Pab import *
from ti_files.NativeFile import NativeFile

logger = logging.getLogger(__name__)


class VariableRecordFile(object):
    def __init__(self, bytes, pab, records=None):
        if records:
            # taking the data from somewhere else, like native file magic
            # bytes needs to be a synthesized header
            self.header = bytes
            self.records = records
            self.currentRecord = 0
            self.recordLength = 80
            self.mode = APPEND
            self.dirty = True
        else:
            self.dirty = False
            self.mode = APPEND if pab is None else mode(pab)
            self.header = bytes[:128]
            self.recordLength = ti_files.recordLength(self.header)
            if self.mode != OUTPUT:
                logger.info("loading existing records: %d", len(bytes))
                self.records = self.__loadRecords(bytes[128:])
            else:
                self.dirty = True
                self.records = []
            if self.mode == APPEND:
                self.currentRecord = len(self.records)
            else:
                self.currentRecord = 0


    @staticmethod
    def create(devname, localPath, pab):
        """ Create a new file, replacing one that might already exist """
        nameParts = str(devname).split(".")
        tiname = nameParts[len(nameParts) - 1]
        recLen = recordLength(pab)
        if recLen == 0:
            recLen = 80
        flags = ti_files.VARIABLE
        if dataType(pab) == INTERNAL:
            flags |= ti_files.INTERNAL
        header = ti_files.createHeader(flags, tiname, bytearray(0))
        ti_files.setRecordLength(header, recLen)
        ti_files.setRecordsPerSector(header, int(256 / recLen))
        return VariableRecordFile(header, pab)


    @staticmethod
    def fromNative(devname, localPath, records):
        flags = ti_files.VARIABLE
        nameParts = str(devname).split(".")
        tiname = nameParts[len(nameParts) - 1]
        header = ti_files.createHeader(flags, tiname, bytearray(0))
        ti_files.setRecordLength(header, 80)
        return VariableRecordFile(header, pab=None, records=records)


    @staticmethod
    def toNative(devname, localPath, bytes):
        logger.info("Loading records from file blocks")
        records = VariableRecordFile(bytes, pab=None).records
        logger.info("record count from file: %d", len(records))
        NativeFile(records, 80, None, None, NativeFlags.TEXT_WINDOWS).writeLines(localPath)


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
                raise Exception("invalid TIFILE")
            # Check that we are a VARIABLE record file
            logger.debug("flags %d", ti_files.flags(fdata))
            if not ti_files.isVariable(fdata):
                raise Exception("file is FIXED, must be VARIABLE")
            if fileType(pab) == RELATIVE:
                raise Exception(
                    "variable length records are restricted to SEQUENTIAL access"
                )
            return VariableRecordFile(fdata, pab)
        except Exception as e:
            logger.exception("not a valid Variable Record TIFILE %s", unix_file_name)
            return None
        finally:
            if fh != None:
                fh.close()

    def isLegal(self, pab):
        return recordType(pab) != FIXED

    def getStatusByte(self):
        statByte = STVARIABLE
        if ti_files.isInternal(self.header):
            statByte |= STINTERNAL
        if self.currentRecord >= len(self.records):
            statByte |= STLEOF
        return statByte

    def restore(self, pab):
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
        logger.info("__loadRecords from bytes: %d", len(bytes))
        records = []
        # variable records return sectors instead of actual record count
        sectors = ti_files.recordCount(self.header)
        sIdx = 0
        offset = 0
        if len(bytes) <= offset:
            return records

        nextoff = offset + bytes[offset] + 1
        record = bytearray(bytes[offset + 1 : nextoff])
        records += [record]

        try:
            while sIdx < sectors:
                logger.debug("record %d of %d", sIdx, sectors)
                offset = nextoff
                if bytes[offset] == 0xFF:
                    sIdx += 1
                    if sIdx >= sectors:
                        break
                    # we need to move to the next ~sector~
                    offset = int((offset / 256) + 1) * 256
                    nextoff = offset + bytes[offset] + 1
                else:
                    nextoff += bytes[offset] + 1
                record = bytearray(bytes[offset + 1 : nextoff])
                records += [record]
        except Exception:
            logger.warn("failed to load all records")
            return []

        return records

    def close(self, localPath):
        if self.dirty:
            try:
                bytes = self.__packRecords()
                fh = open(localPath, "wb")
                fh.write(bytes)
                fh.close()
                self.dirty = False
            except Exception as e:
                logger.exception("Failed to save file %s", localPath)

    def eager_write(self, localPath):
        self.close(localPath)

    def get_bytes(self):
        return self.__packRecords()

    def __packRecords(self):
        sectors = []
        sector = bytearray(256)
        recNo = 0
        offset = 0
        while recNo < len(self.records):
            rec = self.records[recNo]
            recLen = len(rec)
            if (255 - offset) <= (recLen + 1):
                sector[offset] = 0xFF
                sectors += [sector]
                offset = 0
                sector = bytearray(256)
            sector[offset] = recLen
            offset += 1
            if recLen > 0:
                sector[offset : offset + recLen] = rec
                offset += recLen
            recNo += 1

        if offset != 0:
            sector[offset] = 0xFF
            sectors += [sector]
        sectorCount = len(sectors)

        # create a header, and also pack into single bytearray
        header = bytearray(self.header)
        ti_files.setSectors(header, sectorCount)
        ti_files.setEofOffset(header, offset)
        # seems wrong, but isn't
        ti_files.setRecordCount(header, sectorCount)

        bytes = bytearray(128 + (sectorCount * 256))
        bytes[:128] = header
        idx = 128
        sec = 0
        while sec < sectorCount:
            bytes[idx:] = sectors[sec]
            sec += 1
            idx += 256
        return bytes


def load_internal(unix_file_name):
    try:
        pab = bytearray(8)
        pab[1] = (VARIABLE << 4) + (INPUT << 1)
        pab[4] = 80
        return VariableRecordFile.load(unix_file_name, pab).records
    except:
        return []

