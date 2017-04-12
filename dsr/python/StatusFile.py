
import time
from Pab import *
from Status import Status

class StatusFile(object):

    @staticmethod
    def filename():
        return "TIPI.STATUS"

    def __init__(self, tipi_io):
        self.tipi_io = tipi_io
        self.tipiStatus = []
        self.recordNo = 0

    def handle(self, pab, devname):
        op = opcode(pab)
        if op == OPEN:
            self.open(pab, devname)
        elif op == CLOSE:
            self.close(pab, devname)
        elif op == READ:
            self.read(pab, devname)
        else:
            self.tipi_io.send([EOPATTR])

    def close(self, pab, devname):
        self.tipi_io.send([SUCCESS])
        
    def open(self, pab, devname):
        if mode(pab) == INPUT:
            if dataType(pab) == DISPLAY:
                if recordLength(pab) == 0 or recordLength(pab) == 80:
                    self.tipi_io.send([SUCCESS])
                    self.tipi_io.send([80])
                    self.tipiStatus = Status()
                    self.recordNo = 0
                    return
        self.tipi_io.send([EOPATTR])

    def read(self, pab, devname):
        if mode(pab) == INPUT:
            if dataType(pab) == DISPLAY:
                readRec = recordNumber(pab)
                if readRec == 0:
                    readRec = self.recordNo
                else:
                    self.recordNo = readRec

                if readRec >= self.tipiStatus.len():
                    self.tipi_io.send([EEOF])
                    return
                else:
		    fdata = bytearray(self.tipiStatus.record(readRec))
		    self.tipi_io.send([SUCCESS])
		    self.tipi_io.send(fdata)
		    self.recordNo += 1
		    return
        self.tipi_io.send([EOPATTR])



