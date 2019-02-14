import os
import traceback
import pycurl
import logging
from io import BytesIO
from ti_files.ti_files import ti_files
from Pab import *

logger = logging.getLogger(__name__)


class CurlFile(object):

    @staticmethod
    def filename():
        # open file in "input" for GET, "output" for POST
        #   PI.HTTP://ti994a.cwfk.net/tipi.html
        return ("HTTP:", "http:", "HTTPS:", "https:")

    def __init__(self, tipi_io):
        self.tipi_io = tipi_io
        self.bodies = {}
        self.record = {}

    def handle(self, pab, devname):
        logPab(pab)
        op = opcode(pab)
        if op == OPEN:
            self.open(pab, devname)
        elif op == CLOSE:
            self.close(pab, devname)
        elif op == READ:
            self.read(pab, devname)
        elif op == STATUS:
            self.status(pab, devname)
        elif op == LOAD:
            self.load(pab, devname)
        else:
            self.tipi_io.send([EOPATTR])

    def close(self, pab, devname):
        logger.info("close devname - %s", devname)
        self.tipi_io.send([SUCCESS])
        try:
            del(self.bodies[devname])
            del(self.record[devname])
        except BaseException:
            pass

    def open(self, pab, devname):
        logger.info("open devname - %s", devname)
        try:
            url = self.parseDev(devname)
            buffer = BytesIO()
            c = pycurl.Curl()
            c.setopt(c.URL, url)
            c.setopt(c.WRITEDATA, buffer)
            c.perform()
            body = bytearray(buffer.getvalue())
            logger.info("retrieved %d bytes", len(body))
            c.close()
            self.bodies[devname] = body
            self.record[devname] = 0
        except BaseException:
            self.tipi_io.send([EFILERR])
            return

        recLen = recordLength(pab)
        if recLen == 0:
            recLen = 80
        self.tipi_io.send([SUCCESS])
        self.tipi_io.send([recLen])
        return

    def read(self, pab, devname):
        logger.info("read devname - %s", devname)
        try:
            body = self.bodies[devname]
            recLen = recordLength(pab)
            record = recordNumber(pab)
            if record == 0:
                record = self.record[devname]
            lbody = len(body)
            logger.info("length of data: %d", lbody)
            startOff = record * recLen
            if startOff >= lbody:
                self.tipi_io.send([EEOF])
                return
            endOff = (record + 1) * recLen
            if endOff >= lbody:
                endOff = lbody
            logger.info("taking chunk: %d - %d", startOff, endOff)
            fdata = body[startOff:endOff]
            logger.info("record fdata len: %d", len(fdata))
            self.tipi_io.send([SUCCESS])
            self.tipi_io.send(fdata)
            self.record[devname] = record + 1
            return
        except Exception:
            logger.error("issue forming record", print_exc=True)
        self.tipi_io.send([EEOF])
        return

    def status(self, pab, devname):
        logger.info("status devname - %s", devname)
        try:
            recLen = recordLength(pab)
            body = self.bodies[devname]
            record = recordNumber(pab)
            if record == 0:
                record = self.record[devname]
            lbody = len(body)
            startOff = record * recLen

            self.tipi_io.send([SUCCESS])
            statbyte = STVARIABLE
            if startOff >= lbody:
                statbyte |= STLEOF
            self.tipi_io.send([statbyte])
            return
        except Exception:
            logger.error("issue forming record", exc_info=True)
        self.tipi_io.send([EOPATTR])


    def load(self, pab, devname):
        logger.info("load devname - %s", devname)
        try:
            url = self.parseDev(devname)
            logger.debug("url: %s", url)
            buffer = BytesIO()
            c = pycurl.Curl()
            c.setopt(c.URL, url)
            c.setopt(c.WRITEDATA, buffer)
            c.perform()
            c.close()
            body = bytearray(buffer.getvalue())
            logger.debug("downloaded %d bytes", len(body))
            if not ti_files.isValid(body):
                logger.debug("not a TIFILES file")
                self.tipi_io.send([EFILERR])
                return
            if not ti_files.isProgram(body):
                logger.debug("not a PROGRAM image file")
                self.tipi_io.send([EFILERR])
                return
            filesize = ti_files.byteLength(body)
            logger.info("sending program - %d", filesize)
            self.tipi_io.send([SUCCESS])
            self.tipi_io.send((body[128:])[:filesize])
            return
        except BaseException:
            logger.exception("Error loading %s", devname)
        self.tipi_io.send([EFILERR])
        return

    def parseDev(self, devname):
        return str(devname[3:])
