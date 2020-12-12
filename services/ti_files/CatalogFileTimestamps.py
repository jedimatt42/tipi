import os
import io
import sys
import traceback
import math
import logging
from datetime import datetime
from . import NativeFile
from . import ti_files
from . import CatalogFile
from tinames import tinames
from tifloat import tifloat
from Pab import *
from TipiConfig import TipiConfig

logger = logging.getLogger(__name__)

tipi_config = TipiConfig.instance()


class CatalogFileTimestamps(CatalogFile.CatalogFile):
    def __init__(self, localpath, devname):
        super().__init__(localpath, devname, False)

    @staticmethod
    def load(path, pab, devname):
        if mode(pab) == INPUT and dataType(pab) == INTERNAL and recordType(pab) == FIXED:
                if recordLength(pab) == 0 or recordLength(pab) == 146:
                    logger.info("Creating catalog with timestamps")
                    cat = CatalogFileTimestamps(path, devname)
                    cat.loadRecords()
                    return cat
        raise Exception("bad record type")

    def getRecordLength(self):
        return 146

    def encodeVolRecord(self, name, ftype, sectors, recordLength):
        recname = bytearray(tinames.encodeName(name), 'utf-8')
        buff = bytearray(146)

        return self.encodeTimestampedRecord(buff, recname, ftype, sectors, recordLength, None)

    def encodeDirRecord(self, name, ftype, sectors, recordLength):
        recname = bytearray(tinames.asTiShortName(name), 'utf-8')
        buff = bytearray(146)

        if ftype != 6:
            fp = os.path.join(self.localpath, name)
            modTimesinceEpoc = os.path.getmtime(fp)
            dt_timestamp = datetime.fromtimestamp(modTimesinceEpoc)
        else:
            dt_timestamp = None

        return self.encodeTimestampedRecord(buff, recname, ftype, sectors, recordLength, dt_timestamp)

    def encodeTimestamp(self, buff, i, day, month, year, hour, minute, seconds):
        ft = tifloat.asFloat(seconds)
        for b in ft:
            buff[i] = b
            i += 1
        ft = tifloat.asFloat(minute)
        for b in ft:
            buff[i] = b
            i += 1
        ft = tifloat.asFloat(hour)
        for b in ft:
            buff[i] = b
            i += 1
        ft = tifloat.asFloat(day)
        for b in ft:
            buff[i] = b
            i += 1
        ft = tifloat.asFloat(month)
        for b in ft:
            buff[i] = b
            i += 1
        ft = tifloat.asFloat(year)
        for b in ft:
            buff[i] = b
            i += 1
        return i

    def encodeTimestampedRecord(self, buff, recname, ftype, sectors, recordLength, timestamp):
        logger.debug(
            "catalog with timestamp record: %s, %d, %d, %d", recname, ftype, sectors, recordLength
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

        # add a zero timestamp for creation time, cause we don't support it
        i = self.encodeTimestamp(buff, i, 0, 0, 0, 0, 0, 0)

        if timestamp:
            i = self.encodeTimestamp(
                buff, 
                i, 
                timestamp.day, 
                timestamp.month, 
                timestamp.year, 
                timestamp.hour, 
                timestamp.minute, 
                timestamp.second, 
            )
        else:
            # directory and volume entry don't get a modified time
            i = self.encodeTimestamp(buff, i, 0, 0, 0, 0, 0, 0)

        # pad the rest of the fixed record length
        for i in range(i, 146):
            buff[i] = 0

        return buff

