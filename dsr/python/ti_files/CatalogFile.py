import os
import io
import sys
import traceback
import math
import logging
from ti_files import ti_files
from tinames import tinames
from tifloat import tifloat
from Pab import *

logger = logging.getLogger(__name__)

class CatalogFile(object):

    def __init__(self, localpath):
        self.recNum = 0
        self.localpath = localpath

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

    def readRecord(self, pabRecNum):
        if pabRecNum != 0:
            self.recNum = pabRecNum
        record = self.getRecord(self.recNum)
        self.recNum += 1
        return record

    def getRecord(self, idx):
        if idx == 0:
            return self.createVolumeData()
        else:
            return self.createFileCatRecord()

    def createVolumeData(self):
        return self.encodeDirRecord("TIPI", 0, 1440, 1438)

    def createFileCatRecord(self):
        files = sorted(list(filter(lambda x: 
            os.path.isdir(os.path.join(self.localpath, x)) or 
            ti_files.isTiFile(str(os.path.join(self.localpath, x))), os.listdir(self.localpath))))
        fh = None
        try:
            if self.recNum - 1 >= len(files):
                return self.encodeDirRecord("", 0, 0, 0)

            f = files[self.recNum - 1]

            if os.path.isdir(os.path.join(self.localpath, f)):
                return self.encodeDirRecord(f, 6, 2, 0)

            fh = open(os.path.join(self.localpath, f), 'rb')

            header = bytearray(fh.read()[:128])

            ft = ti_files.dsrFileType(header)
            sectors = ti_files.getSectors(header) + 1
            recordlen = ti_files.recordLength(header)
            return self.encodeDirRecord(f, ft, sectors, recordlen)

        except Exception as e:
            traceback.print_exc()
            raise

        finally:
            if fh is not None:
                fh.close()

    def encodeDirRecord(self, name, ftype, sectors, recordLength):
        bytes = bytearray(38)

        shortname = tinames.asTiShortName(name)

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
