
import logging
from Pab import *
from datetime import datetime

logger = logging.getLogger(__name__)

class ClockFile(object):

    @staticmethod
    def filename():
        return "PIO"

    def __init__(self, tipi_io):
        self.tipi_io = tipi_io

    def handle(self, pab, devname):
        op = opcode(pab)
        if op == OPEN:
            self.open(pab, devname)
        elif op == CLOSE:
            self.close(pab, devname)
        elif op == WRITE:
            self.write(pab, devname)
        else:
            self.tipi_io.send([EOPATTR])

    def close(self, pab, devname):
        logger.info("close special? {}".format(devname))
        self.data_filename = None
        # todo: trigger conversion to PDF
        self.tipi_io.send([SUCCESS])

    def open(self, pab, devname):
        self.CR = 1
        self.LF = 1
        dev_options = devname.split('.')
        for o in dev_options:
            if o == 'LF':
                self.LF = 0
            if o == 'CR':
                self.CR = 0
                self.LF = 0
        if mode(pab) == OUTPUT or mode(pab) == UPDATE:
            self.data_filename = '/tmp/print_' + datetime.today().isoformat()[:-7].epson
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
        self.tipi_io.send([SUCCESS])
        data = str(self.tipi_io.receive())
        with open(self.data_filename, 'ab') as data_file:
            data_file.write(data)
            if self.CR:
                data_file.write(0x13)
            if self.LF:
                data_file.write(0x10)
        self.tipi_io.send([SUCCESS])



