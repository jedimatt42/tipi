import sys
import traceback
import logging
import time
import os
import errno

from ti_files.ti_files import ti_files
from ti_files.ProgramImageFile import ProgramImageFile
from ti_files.FixedRecordFile import FixedRecordFile
from ti_files.VariableRecordFile import VariableRecordFile
from ti_files.CatalogFile import CatalogFile
from ti_files.NativeFile import NativeFile
from ti_files.BasicFile import BasicFile
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
        self.openFiles = {}

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

        if os.path.isdir(localPath):
            try:
                self.sendSuccess()
                cat_file = CatalogFile.load(localPath, pab)
                self.tipi_io.send([cat_file.getRecordLength()])
                self.openFiles[localPath] = cat_file
                return
            except Exception as e:
                self.sendErrorCode(EOPATTR)
                logger.exception("failed to open dir - %s", devname)
                return

        if os.path.exists(localPath):
            try:
                open_file = None
                if ti_files.isTiFile(localPath):
                    if recordType(pab) == FIXED:
                        open_file = FixedRecordFile.load(localPath, pab)
                    else:
                        open_file = VariableRecordFile.load(localPath, pab)
                else:
                    open_file = NativeFile.load(localPath, pab)

                fillInRecordLen = open_file.getRecordLength()

                self.sendSuccess()
                self.tipi_io.send([fillInRecordLen])
                self.openFiles[localPath] = open_file
                return

            except Exception as e:
                self.sendErrorCode(EOPATTR)
                logger.exception("failed to open file - %s", devname)
                return


        else:
            # TODO: here we can handle creation of new files.
            pass
            # TODO: check that any parent directory specified does exist.

        self.sendErrorCode(EFILERR)

    def handleClose(self, pab, devname):
        logger.debug("Opcode 1 Close - %s", devname)
        logPab(pab)
        self.sendSuccess()
        try:
            del self.openFiles[tinames.devnameToLocal(devname)]
        except Exception as e:
            pass

    def handleRead(self, pab, devname):
        logger.debug("Opcode 2 Read - %s", devname)
        logPab(pab)
        localPath = tinames.devnameToLocal(devname)

        if not os.path.exists(localPath):
            logger.debug("file %s does not exist", localPath)
            self.sendErrorCode(EFILERR)
            return

        try:
            open_file = self.openFiles[localPath]

            recNum = recordNumber(pab)
            if not open_file.isLegal(pab):
                logger.error("illegal read mode for %s", devname)
                self.sendErrorCode(EFILERR)
                return

            rdata = open_file.readRecord(recNum)
            if rdata is None:
                logger.debug("received None for record %d", recNum)
                self.sendErrorCode(EEOF)
            else:
                self.sendSuccess()
                self.tipi_io.send(rdata)
            return
        except Exception as e:
            traceback.print_exc()
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
            if unix_name.lower().endswith((".bas", ".xb")):
                prog_file = BasicFile.load(unix_name)
            else:
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

    def parentExists(self, unix_name):
        parent = os.path.dirname(unix_name)
        return os.path.exists(parent) and os.path.isdir(parent)
