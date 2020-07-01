import logging
import os
from Pab import *
from datetime import datetime
from subprocess import call

logger = logging.getLogger(__name__)

crlf = bytearray(2)
crlf[0] = 13
crlf[1] = 10


class PioFile(object):
    @staticmethod
    def filename():
        return "PIO"

    def __init__(self, tipi_io):
        self.tipi_io = tipi_io
        self.data_filename = None
        self.last_record = bytearray(0)

    def handle(self, pab, devname):
        op = opcode(pab)
        if op == OPEN:
            self.open(pab, devname)
        elif op == CLOSE:
            self.close(pab, devname)
        elif op == WRITE:
            self.write(pab, devname)
        elif op == READ:
            self.read(pab, devname)
        elif op == STATUS:
            self.status(pab, devname)
        else:
            self.tipi_io.send([EOPATTR])

    def close(self, pab, devname):
        logger.info("close special? {}".format(devname))
        dev_options = devname.split(".")
        if not "SP" in dev_options:
            # make sure we've at least had one CR or the converter won't do anything.
            if not 0x0D in self.last_record:
                with open(self.data_filename, "ab") as data_file:
                    data_file.write(crlf)
            # spawn conversion to PDF
            self.convert(self.data_filename)
            self.data_filename = None
            self.last_record = bytearray(0)
        self.tipi_io.send([SUCCESS])

    def open(self, pab, devname):
        logger.info("open special? {}".format(devname))
        self.CR = 1
        self.LF = 1
        self.NU = 0
        self.last_record = bytearray(0)
        dev_options = devname.split(".")
        for o in dev_options:
            if o == "LF":
                self.LF = 0
            if o == "CR":
                self.CR = 0
                self.LF = 0
            if o == "NU":
                self.NU = 1
        if mode(pab) == OUTPUT or mode(pab) == UPDATE:
            if self.data_filename is None:
                spools = [f for f in os.listdir("/tmp/") if f.startswith("print_")]
                if len(spools) == 1:
                    self.data_filename = "/tmp/" + spools[0]
                    logger.info("continuing with spool: {}".format(self.data_filename))
                else:
                    if "A4" in dev_options:
                        paper = "_a4"
                    else:
                        paper = ""
                    self.data_filename = (
                        "/tmp/print_"
                        + datetime.today().strftime("%Y_%m_%d_T%H_%M_%S")
                        + paper
                        + ".prn"
                    )
                    logger.info("creating new spool: {}".format(self.data_filename))
            else:
                logger.info("continuing with spool: {}".format(self.data_filename))

            if recordLength(pab) == 0 or recordLength(pab) == 80:
                self.tipi_io.send([SUCCESS])
                self.tipi_io.send([80])
                return
            else:
                reclen = recordLength(pab)
                self.tipi_io.send([SUCCESS])
                self.tipi_io.send([reclen])
                return
        self.tipi_io.send([EOPATTR])

    def write(self, pab, devname):
        logger.info("write special? {}".format(devname))
        self.tipi_io.send([SUCCESS])
        data = self.tipi_io.receive()
        self.last_record = data
        with open(self.data_filename, "ab") as data_file:
            data_file.write(data)
            if self.CR:
                data_file.write(crlf[:-1])
            if self.LF:
                data_file.write(crlf[1:])
            if self.NU:
                # pad line ending with 6 nulls to allow time for carriage return action
                data_file.write(bytearray(6))
        self.tipi_io.send([SUCCESS])

    def read(self, pab, devname):
        logger.info("read special? {}".format(devname))

    def status(self, pab, devname):
        logger.info("status special? {}".format(devname))

    def convert(self, prn_name):
        if os.environ.get('TIPI_WEBSOCK'):
            logger.info("skipping PDF conversion")
            return
        logger.info("converting {} to PDF".format(prn_name))
        callargs = ["/home/tipi/tipi/services/epson.sh", prn_name]
        if call(callargs) != 0:
            logger.error("failed to convert to pdf: {}".format(prn_name))
        else:
            logger.info("completed pdf conversion")
