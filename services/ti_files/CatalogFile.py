import os
import io
import sys
import traceback
import math
import logging
from . import NativeFile
from . import ti_files
from tinames import tinames
from tinames import NativeFlags
from tifloat import tifloat
from Pab import *
from TipiConfig import TipiConfig

logger = logging.getLogger(__name__)

tipi_config = TipiConfig.instance()


class CatalogFile(object):
    def __init__(self, localpath, devname, long):
        self.recNum = 0
        self.localpath = localpath
        self.devname = devname
        self.longnames = long
        self.records = []
        self.isNativeTextDir = tinames.nativeFlags(devname) == NativeFlags.TEXT_WINDOWS

    @staticmethod
    def load(path, pab, devname):
        if mode(pab) == INPUT and dataType(pab) == INTERNAL:
            if recordType(pab) == FIXED:
                # since it is a directory the recordlength is 38, often it is opened with no value.
                # TODO: if they specify the longer filename record length, and recordType, then this will be different
                #       for implementation of long file name handling
                if recordLength(pab) == 0 or recordLength(pab) == 38:
                    # TODO: load all the directory records upfront
                    cat = CatalogFile(path, devname, False)
                    cat.loadRecords()
                    return cat
            if recordType(pab) == VARIABLE and recordLength(pab) == 0:
                cat = CatalogFile(path, devname, True)
                cat.loadRecords()
                return cat
        raise Exception("bad record type")

    def getRecordLength(self):
        if not self.longnames:
            return 38
        else:
            reclen = 0
            for rec in self.records:
                reclen = max(reclen, len(rec))
            return reclen

    def isLegal(self, pab):
        return mode(pab) == INPUT and dataType(pab) == INTERNAL

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

    def loadRecords(self):
        recs = []
        recs += [self.createVolumeData()]
        recs += self.createFileCatRecords()
        recs += [self.encodeDirRecord("", 0, 0, 0)]
        self.records = recs

    def createVolumeData(self):
        logger.debug("localpath: %s", self.localpath)
        volumeName = os.path.basename(self.localpath)
        logger.debug("volumeName stage1: %s", volumeName)

        try:
            sector_count = max(2, min(9999, int(tipi_config.get("SECTOR_COUNT"))))
        except:
            sector_count = 1440

        if self.devname == "DSK.":
            return self.encodeVolRecord("", 0, sector_count, sector_count - 2)

        if self.localpath == "/home/tipi/tipi_disk":
            volumeName = "TIPI"
        elif self.devname.startswith(("DSK.")):
            volumeName = self.devname.split(".")[1]
        else:
            drive = self.devname.split(".")[0]
            if drive == "TIPI" or drive == "DSK0":
                volumeName = "TIPI"
            else:
                parts = tipi_config.get(drive + "_DIR").split(".")
                volumeName = parts[-1]

        logger.debug("volumeName: %s", volumeName)
        return self.encodeVolRecord(volumeName, 0, sector_count, sector_count - 2)

    def createFileCatRecords(self):
        if self.devname == "DSK.":
            return {}

        dir_sort = tipi_config.get("DIR_SORT")
        if dir_sort not in ("MIXED", "FIRST", "LAST"):
            dir_sort = "FIRST"

        if dir_sort == "MIXED":
            files = sorted(
                list(
                    filter(
                        lambda x: self.include(os.path.join(self.localpath, x)),
                        os.listdir(self.localpath),
                    )
                )
            )
        else:
            dirs = sorted(
                list(
                    filter(
                        lambda x: self.includedirs(os.path.join(self.localpath, x)),
                        os.listdir(self.localpath),
                    )
                )
            )
            files = sorted(
                list(
                    filter(
                        lambda x: self.includefiles(os.path.join(self.localpath, x)),
                        os.listdir(self.localpath),
                    )
                )
            )
            if dir_sort == "FIRST":
                files = dirs + files
            elif dir_sort == "LAST":
                files += dirs

        return map(self.createFileRecord, files)

    def include(self, fp):
        logger.debug("include %s", fp)
        return os.path.isdir(fp) or ti_files.isTiFile(fp) or (
                os.path.isfile(fp) and not fp.endswith('.sectors'))

    def includefiles(self, fp):
        logger.debug("includefiles %s", fp)
        return ti_files.isTiFile(fp) or (
                os.path.isfile(fp) and not fp.endswith('.sectors'))

    def includedirs(self, fp):
        logger.debug("includedirs %s", fp)
        return os.path.isdir(fp)

    def createFileRecord(self, f):
        logger.debug("createFileRecord %s", f)
        fh = None
        try:
            fp = os.path.join(self.localpath, f)
            if os.path.isdir(fp):
                return self.encodeDirRecord(f, 6, 2, 0)

            if ti_files.isTiFile(fp):
                fh = open(fp, "rb")

                header = bytearray(fh.read()[:128])

                ft = ti_files.catFileType(header)
                sectors = ti_files.getSectors(header) + 1
                recordlen = ti_files.recordLength(header)
                return self.encodeDirRecord(f, ft, sectors, recordlen)
            # else it is a native file
            elif fp.lower().endswith(NativeFile.dv80suffixes) or self.isNativeTextDir:
                # dis/var
                ft = 2
                recCount = self.line_count(fp)
                recSize = 80
            else:
                # dis/fix
                ft = 1
                stats = os.stat(fp)
                recCount = stats.st_size / 128 + 1
                recSize = 128
            return self.encodeDirRecord(f, ft, recCount, recSize)

        except Exception as e:
            traceback.print_exc()
            raise

        finally:
            if fh is not None:
                fh.close()

    def encodeVolRecord(self, name, ftype, sectors, recordLength):
        if self.longnames:
            recname = bytearray(name, 'utf-8')
            buff = bytearray(28 + len(recname))
        else:
            recname = bytearray(tinames.encodeName(name), 'utf-8')
            buff = bytearray(38)

        return self.encodeCatRecord(buff, recname, ftype, sectors, recordLength)

    def encodeDirRecord(self, name, ftype, sectors, recordLength):
        if self.longnames:
            recname = bytearray(name, 'utf-8')
            buff = bytearray(28 + len(recname))
        else:
            recname = bytearray(tinames.asTiShortName(name), 'utf-8')
            buff = bytearray(38)

        return self.encodeCatRecord(buff, recname, ftype, sectors, recordLength)

    def encodeCatRecord(self, buff, recname, ftype, sectors, recordLength):
        logger.debug(
            "cat record: %s, %d, %d, %d", recname, ftype, sectors, recordLength
        )

        buff[0] = len(recname)
        i = 1
        for c in recname:
            buff[i] = c
            i += 1
        ft = tifloat.asFloat(ftype)
        for b in ft:
            buff[i] = b
            i += 1
        sc = tifloat.asFloat(sectors)
        for b in sc:
            buff[i] = b
            i += 1
        rl = tifloat.asFloat(recordLength)
        for b in rl:
            buff[i] = b
            i += 1
        if not self.longnames:
            # pad the rest of the fixed record length
            for i in range(i, 38):
                buff[i] = 0

        return buff

    def line_count(self, fp):
        i = 0
        with open(fp, encoding='utf-8', errors='ignore') as f:
            for i, l in enumerate(f):
                pass
        return i + 1
