import os
import subprocess
import traceback
import logging
from ti_files import ti_files
from Pab import *
from ti_files.NativeFile import NativeFile
from ti_files.BasicFile import BasicFile, basicSuffixes
from ti_files.ProgramImageFile import ProgramImageFile
from ti_files.FixedRecordFile import FixedRecordFile
from ti_files.VariableRecordFile import VariableRecordFile

logger = logging.getLogger(__name__)

tipi_dir = os.getenv("TIPI_DIR")


class CurlFile(object):

    @staticmethod
    def filename():
        # open file in "input" for GET
        #   PI.HTTP://ti994a.cwfk.net/tipi.html
        return ("HTTP:", "http:", "HTTPS:", "https:")

    def __init__(self, tipi_io):
        self.tipi_io = tipi_io
        self.files = {}

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
        elif op == SAVE:
            self.save(pab, devname)
        elif op == RESTORE:
            self.restore(pab, devname)
        else:
            self.tipi_io.send([EOPATTR])

    def close(self, pab, devname):
        logger.info("close devname - %s", devname)
        self.tipi_io.send([SUCCESS])
        try:
            del(self.files[devname])
        except BaseException:
            pass

    def open(self, pab, devname):
        logger.info("open devname - %s", devname)
        try:
            url = self.parseDev(devname)
            logger.info("url: %s", url)
            file = self.fetch(url, pab)
            self.files[devname] = file
        except BaseException:
            logger.exception("failed")
            self.tipi_io.send([EFILERR])
            return

        recLen = recordLength(pab)
        if recLen == 0:
            recLen = file.getRecordLength()
        self.tipi_io.send([SUCCESS])
        self.tipi_io.send([recLen])
        return

    def restore(self, pab, devname):
        try:
            open_file = self.files[devname]
        except KeyError:
            pass

        if open_file == None:
            self.tipi_io.send([EFILERR])
            return

        open_file.restore(pab)
        self.tipi_io.send([SUCCESS])


    def read(self, pab, devname):
        logger.info("read devname - %s", devname)
        try:
            open_file = self.files[devname]

            if not open_file.isLegal(pab):
                logger.error("illegal read mode for %s", devname)
                self.tipi_io.send([EFILERR])
                return

            recNum = recordNumber(pab)
            rdata = open_file.readRecord(recNum)
            if rdata is None:
                logger.info("received None for record %d", recNum)
                self.tipi_io.send([EEOF])
            else:
                self.tipi_io.send([SUCCESS])
                self.tipi_io.send(rdata)
                logger.info("record bytes: %d", len(rdata))
            return
        except Exception:
            logger.exception("failed to read from open file")
            self.tipi_io.send([EFILERR])

    def status(self, pab, devname):
        logger.info("status devname - %s", devname)
        statbyte = 0

        try:
            open_file = self.files[devname]
            statbyte = open_file.getStatusByte()
        except KeyError:
            statbyte = NativeFile.status("", devname)

	# not really implemented yet
        self.tipi_io.send([SUCCESS])
        self.tipi_io.send([statbyte])

    def load(self, pab, devname):
        logger.info("load devname - %s", devname)
        try:
            url = self.parseDev(devname)
            tmpname = self.http_get(url, pab)

            if (not ti_files.isTiFile(tmpname)) and devname.lower().endswith(basicSuffixes):
                prog_file = BasicFile.load(tmpname)
            else:
                prog_file = ProgramImageFile.load(tmpname)

            filesize = prog_file.getImageSize()
            bytes = prog_file.getImage()
            maxsize = recordNumber(pab)
            if filesize > maxsize:
                logger.debug("TI buffer too small, only loading %d of %d bytes", maxsize, filesize)
                bytes = bytes[:maxsize]

            self.tipi_io.send([SUCCESS])
            logger.info("LOAD image size %d", filesize)
            self.tipi_io.send(bytes)

        except Exception:
            # I don't think this will work. we need to check for as
            #   many errors as possible up front.
            self.tipi_io.send([EFILERR])
            logger.exception("failed to load file - %s", devname)

    def save(self, pab, devname):
        logger.info("save devname - %s", devname)
        try:
            url = self.parseDev(devname)
            tmpname = '/tmp/CF'

            self.tipi_io.send([SUCCESS])
            fdata = self.tipi_io.receive()
            logger.debug("received program image")

            if devname.lower().endswith(basicSuffixes):
                prog_file = BasicFile.create(fdata)
            else:
                prog_file = ProgramImageFile.create(devname, tmpname, fdata)
            logger.debug("created file object")
            prog_file.save(tmpname)

            self.http_post(url, pab)

            self.tipi_io.send([SUCCESS])
        except Exception as e:
            logger.exception("failed to save PROGRAM")
            self.tipi_io.send([EFILERR])
        return


    def agent_str(self):
        version = "unknown"
        with open(f"{tipi_dir}/version.txt", "r") as v_in:
            for line in v_in.readlines():
                parts = line.split("=")
                if str(parts[0]).strip().upper() == "VERSION":
                    version = str(parts[1]).strip()

        return "ti994a-Tipi/{}".format(version)

    def http_get(self, url, pab):
        agent = self.agent_str()

        tmpname = '/tmp/CF'
    
        cmd = "/usr/bin/wget --user-agent={} -O {} {}".format(agent, tmpname, url)
        logger.info("cmd: %s", cmd)
        code = os.system(cmd)
        if code != 0:
            raise Exception("error downloading resource")
        return tmpname

    def fetch(self, url, pab):
        tmpname = self.http_get(url, pab)
        if ti_files.isTiFile(tmpname):
            if recordType(pab) == FIXED:
                return FixedRecordFile.load(tmpname, pab)
            else:
                return VariableRecordFile.load(tmpname, pab)
        else:
            return NativeFile.load(tmpname, pab, "", url)

    def http_post(self, url, pab):
        agent = self.agent_str()

        tmpname = '/tmp/CF'

        cmd = "/usr/bin/curl -v -A {} -F 'TIFILES=@{}' {} -o /dev/null".format(agent, tmpname, url)
        logger.info("cmd: %s", cmd)
        output = subprocess.getoutput(cmd)

        logger.info("output: %s", output)

        # ensure the server responds with a 200 series status code
        if not '< HTTP/1.1 2' in output:
            raise Exception("error uploading resource")

    def parseDev(self, devname):
        return str(devname[3:])
