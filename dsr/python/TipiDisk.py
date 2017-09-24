import sys
import traceback
import logging
import time
import os
import errno

from ti_files import ti_files
from ti_files.ProgramImageFile import ProgramImageFile
from array import array
from tipi.TipiMessage import TipiMessage
from tifloat import tifloat
from tinames import tinames
from SpecialFiles import SpecialFiles
from Pab import *

logger = logging.getLogger(__name__)
oled = logging.getLogger('oled')


class TipiDisk(object):

    def __init__(self, tipi_io):
        self.tipi_io = tipi_io
        self.openRecord = {}

    #
    # Entry point to process all disk pab requests.
    def handle(self, pab, filename):
        switcher = {
            0: self.handleOpen,
            1: self.handleClose,
            2: self.handleRead,
            3: self.handleWrite,
            4: self.handleRestore,
            5: self.handleLoad,
            6: self.handleSave,
            7: self.handleDelete,
            8: self.handleScratch,
            9: self.handleStatus
        }
        handler = switcher.get(opcode(pab), self.handleNotSupported)
        handler(pab, filename)

    #
    # Utils
    #

    def handleNotSupported(self, pab, devname):
        logger.warn("Opcode not supported: " + str(opcode(pab)))
        self.sendErrorCode(EILLOP)

    def sendErrorCode(self, code):
        logger.error("responding with error: " + str(code))
        self.sendSingleByte(code)

    def sendSuccess(self):
        logger.debug("responding with success!")
        self.sendSingleByte(SUCCESS)

    def sendSingleByte(self, byte):
        msg = bytearray(1)
        msg[0] = byte
        self.tipi_io.send(msg)

    def handleOpen(self, pab, devname):
        logger.debug("Opcode 0 Open - %s", devname)
        logPab(pab)
        localPath = tinames.devnameToLocal(devname)
        logger.debug("  local file: " + localPath)
        if mode(pab) == INPUT and not os.path.exists(localPath):
            self.sendErrorCode(EFILERR)
            return

        if os.path.isdir(localPath) and mode(pab) == INPUT and dataType(
                pab) == INTERNAL and recordType(pab) == FIXED:
            self.sendSuccess()
            # since it is a directory the recordlength is 38, often it is opened with no value.
            # TODO: if they specify the longer filename record length, and recordType, then this will be different
            #       for implementation of long file name handling
            self.tipi_io.send([38])
            self.openRecord[localPath] = 0
            return

        if os.path.exists(localPath):
            fh = None
            try:
                fh = open(localPath, 'rb')
                bytes = bytearray(fh.read())
                if not ti_files.isValid(bytes):
                    raise Exception("not tifiles format")
                if dataType(pab) == DISPLAY and ti_files.isInternal(bytes):
                    raise Exception("cannot open as DISPLAY")
                if dataType(
                        pab) == INTERNAL and not ti_files.isInternal(bytes):
                    raise Exception("cannot open as INTERNAL")
                if recordType(pab) == FIXED and ti_files.isVariable(bytes):
                    raise Exception("cannot open as FIXED")
                if recordType(
                        pab) == VARIABLE and not ti_files.isVariable(bytes):
                    raise Exception("cannot open as VARIABLE")
                if recordLength(pab) != 0 and (
                        ti_files.recordLength(bytes) != recordLength(pab)):
                    raise Exception("record length mismatch")
                fillInRecordLen = ti_files.recordLength(bytes)

                self.sendSuccess()
                self.tipi_io.send([fillInRecordLen])
                self.openRecord[localPath] = 0
                return

            except Exception as e:
                self.sendErrorCode(EOPATTR)
                logger.exception("failed to open file - %s", devname)
                return
            finally:
                if fh is not None:
                    fh.close()

        else:
            pass
            # TODO: check that any parent directory specified does exist.

        self.sendErrorCode(EFILERR)

    def handleClose(self, pab, devname):
        logger.debug("Opcode 1 Close - %s", devname)
        logPab(pab)
        self.sendSuccess()
        try:
            del self.openRecord[tinames.devnameToLocal(devname)]
        except Exception as e:
            # I don't care if close is called while file is not open
            pass

    def handleRead(self, pab, devname):
        logger.debug("Opcode 2 Read - %s", devname)
        logPab(pab)
        localPath = tinames.devnameToLocal(devname)

        if not os.path.exists(localPath):
            logger.debug("file %s does not exist", localPath)
            self.sendErrorCode(EFILERR)
            return

        recNum = recordNumber(pab)
        # UNSPEC'ED
        # TI software is too lazy to increment record number because TIFDC
        # didn't require it.
        if recNum == 0:
            recNum = self.openRecord[localPath]

        if os.path.isdir(localPath) and mode(pab) == INPUT and dataType(
                pab) == INTERNAL and recordType(pab) == FIXED:
            logger.debug("  local file: %s", localPath)

            try:
                if recNum == 0:
                    self.sendSuccess()
                    vdata = self.createVolumeData(localPath)
                    self.tipi_io.send(vdata)
                    return
                else:
                    fdata = self.createFileCatRecord(localPath, recNum)
                    if len(fdata) == 0:
                        self.sendErrorCode(EEOF)
                    else:
                        self.sendSuccess()
                    self.tipi_io.send(fdata)
                    return
            except BaseException:
                pass
            finally:
                self.openRecord[localPath] += 1

        if os.path.exists(localPath):
            fdata = self.createFileReadRecord(localPath, recNum)
            if fdata is None:
                self.sendErrorCode(EEOF)
            else:
                self.sendSuccess()
                self.tipi_io.send(fdata)
                self.openRecord[localPath] += 1
            return

        self.sendErrorCode(EFILERR)

    def handleWrite(self, pab, devname):
        logger.info("Opcode 3 Write - %s", devname)
        logPab(pab)
        self.sendErrorCode(EDEVERR)

    def handleRestore(self, pab, devname):
        logger.info("Opcode 4 Restore - %s", devname)
        logPab(pab)
        self.sendErrorCode(EDEVERR)

    def handleLoad(self, pab, devname):
        logger.info("Opcode 5 LOAD - %s", devname)
        logPab(pab)
        maxsize = recordNumber(pab)
        unix_name = tinames.devnameToLocal(devname)
        try:
            prog_file = ProgramImageFile.load(unix_name)
            filesize = prog_file.getImageSize()
            if filesize > maxsize:
                logger.debug("TI buffer too small")
                self.tipi_io.sendErrorCode(EFILERR)
                return

            bytes = prog_file.getImage()
            self.sendSuccess()
            logger.info("LOAD image size %d", filesize)
            self.tipi_io.send(bytes)

        except Exception as e:
            # I don't think this will work. we need to check for as
            #   many errors as possible up front.
            self.sendErrorCode(EFILERR)
            logger.exception("failed to load file - %s", devname)

    def handleSave(self, pab, devname):
        logger.info("Opcode 6 Save - %s", devname)
        logPab(pab)
        unix_name = tinames.devnameToLocal(devname)
        if self.parentExists(unix_name):
            self.sendSuccess()
            fdata = self.tipi_io.receive()
            try:
                prog_file = ProgramImageFile.create(devname, unix_name, fdata)
                prog_file.save(unix_name)
                # TODO: modify DSR to expect a response after sending the bytes down.
                # self.sendSuccess()
            except Exception as e:
                traceback.print_exc()
                self.sendErrorCode(EDEVERR)
            return
        self.sendErrorCode(EDEVERR)

    def handleDelete(self, pab, devname):
        logger.info("Opcode 7 Delete - %s", devname)
        logPab(pab)
        logger.info("Delete not implemented yet")
        self.sendErrorCode(EDEVERR)

    def handleScratch(self, pab, devname):
        logger.info("Opcode 8 Scratch - %s", devname)
        logPab(pab)
        self.sendErrorCode(EDEVERR)

    def handleStatus(self, pab, devname):
        logger.info("Opcode 9 Status - %s", devname)
        logPab(pab)
        logger.info("Status not implemented yet")
        self.sendErrorCode(EDEVERR)

    def createVolumeData(self, path):
        return self.encodeDirRecord("TIPI", 0, 1440, 1438)

    def createFileCatRecord(self, path, recordNumber):
        files = sorted(list(filter(lambda x: os.path.isdir(os.path.join(
            path, x)) or ti_files.isTiFile(str(os.path.join(path, x))), os.listdir(path))))
        fh = None
        try:
            f = files[recordNumber - 1]

            if os.path.isdir(os.path.join(path, f)):
                return self.encodeDirRecord(f, 6, 2, 0)

            fh = open(os.path.join(path, f), 'rb')

            header = bytearray(fh.read()[:128])

            ft = ti_files.dsrFileType(header)
            sectors = ti_files.getSectors(header) + 1
            recordlen = ti_files.recordLength(header)
            return self.encodeDirRecord(f, ft, sectors, recordlen)

        except Exception as e:
            return self.encodeDirRecord("", 0, 0, 0)

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

    def createFileReadRecord(self, path, recordNumber):
        logger.debug("loading record %d from %s", recordNumber, path)
        fh = None
        try:
            fh = open(path, 'rb')
            bytes = bytearray(fh.read())
            return ti_files.readRecord(bytes, recordNumber)
        except BaseException:
            raise
        finally:
            if fh is not None:
                fh.close()
        return None

    def parentExists(self, unix_name):
        parent = os.path.dirname(unix_name)
        return os.path.exists(parent) and os.path.isdir(parent)
