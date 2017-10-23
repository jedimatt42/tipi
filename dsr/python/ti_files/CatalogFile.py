import os
import io
import sys
import traceback
import math
import logging
import NativeFile
from ti_files import ti_files
from tinames import tinames
from tifloat import tifloat
from Pab import *

logger = logging.getLogger(__name__)

class CatalogFile(object):

    def __init__(self, localpath):
        self.recNum = 0
        self.localpath = localpath
        self.records = self.__loadRecords()

    @staticmethod
    def load(path, pab):
        if mode(pab) == INPUT and dataType(pab) == INTERNAL and recordType(pab) == FIXED:
            # since it is a directory the recordlength is 38, often it is opened with no value.
            # TODO: if they specify the longer filename record length, and recordType, then this will be different
            #       for implementation of long file name handling
            if recordLength(pab) == 0 or recordLength(pab) == 38:
                # TODO: load all the directory records upfront
                return CatalogFile(path)

    def getRecordLength(self):
        return 38

    def isLegal(self, pab):
        return mode(pab) == INPUT and dataType(pab) == INTERNAL and recordType(pab) == FIXED

    def close(self, localPath):
        pass

    def readRecord(self, pabRecNum):
        if pabRecNum != 0:
            self.recNum = pabRecNum
        record = self.getRecord(self.recNum)
        self.recNum += 1
        return record

    def getRecord(self, idx):
        if idx >= len(self.records):
            return None
        return self.records[idx]

    def __loadRecords(self):
        recs = []
        recs += [ self.__createVolumeData() ]
        recs += self.__createFileCatRecords()
        recs += [ self.__encodeDirRecord("", 0, 0, 0) ]
        return recs

    def __createVolumeData(self):
        return self.__encodeDirRecord("TIPI", 0, 1440, 1438)

    def __createFileCatRecords(self):
        files = sorted(list(filter(lambda x: 
            self.__include(os.path.join(self.localpath, x)), os.listdir(self.localpath))))
        return map(self.__createFileRecord, files)

    def __include(self, fp):
        logger.debug("__include %s", fp)
        return os.path.isdir(fp) or ti_files.isTiFile(fp) or os.path.isfile(fp)

    def __createFileRecord(self, f):
        logger.debug("createFileRecord %s", f)
        fh = None
        try:
            fp = os.path.join(self.localpath, f)
            if os.path.isdir(fp):
                return self.__encodeDirRecord(f, 6, 2, 0)

            if ti_files.isTiFile(fp):
                fh = open(fp, 'rb')

                header = bytearray(fh.read()[:128])

                ft = ti_files.dsrFileType(header)
                sectors = ti_files.getSectors(header) + 1
                recordlen = ti_files.recordLength(header)
                return self.__encodeDirRecord(f, ft, sectors, recordlen)

            # else it is a native file
            if fp.lower().endswith(NativeFile.dv80suffixes):
                # dis/var
                ft = 2
                recCount = self.__line_count(fp)
                recSize = 80
            else:
                # dis/fix
                ft = 1
                stats = os.stat(fp)
                recCount = stats.st_size / 128 + 1
                recSize = 128
            return self.__encodeDirRecord(f, ft, recCount, recSize)

        except Exception as e:
            traceback.print_exc()
            raise

        finally:
            if fh is not None:
                fh.close()

    def __encodeDirRecord(self, name, ftype, sectors, recordLength):
        bytes = bytearray(38)

        shortname = tinames.asTiShortName(name)
        logger.debug("cat record: %s, %d, %d, %d", shortname, ftype, sectors, recordLength)

        bytes[0] = len(shortname)
        i = 1
        for c in shortname:
            bytes[i] = c
            i += 1
        ft = tifloat.asFloat(ftype)
        for b in ft:
            bytes[i] = b
            i += 1
        sc = tifloat.asFloat(sectors)
        for b in sc:
            bytes[i] = b
            i += 1
        rl = tifloat.asFloat(recordLength)
        for b in rl:
            bytes[i] = b
            i += 1
        for i in range(i, 38):
            bytes[i] = 0

        return bytes

    def __line_count(self, fp):
        i = 0
        with open(fp) as f:
            for i, l in enumerate(f):
                pass
        return i + 1