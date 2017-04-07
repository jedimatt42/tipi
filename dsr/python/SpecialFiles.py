
import time
from Pab import *
import socket

class SpecialFiles(object):

    def __init__(self, tipi_io):
        self.tipi_io = tipi_io
        self.tipiStatus = []
        self.recordNo = 0

    def open(self, pab, devname):
        print "open special? {}".format(devname)
        return self.openClock(pab, devname) or self.openStatus(pab, devname)
        
    def read(self, pab, devname):
        print "read special? {}".format(devname)
        return self.readClock(pab, devname) or self.readStatus(pab, devname)

    def openClock(self, pab, devname):
        if devname == "TIPI.CLOCK" and mode(pab) == INPUT:
            if dataType(pab) == DISPLAY:
                if recordLength(pab) == 0 or recordLength(pab) == 24:
                    self.tipi_io.send([SUCCESS])
                    self.tipi_io.send([24])
                    return True
                else:
                    self.tipi_io.send([EOPATTR])
                    return True
        return False

    def readClock(self, pab, devname):
        if devname == "TIPI.CLOCK" and mode(pab) == INPUT:
            if dataType(pab) == DISPLAY:
                fdata = bytearray(time.asctime())
                self.tipi_io.send([SUCCESS])
                self.tipi_io.send(fdata)
                return True
        return False

    def openStatus(self, pab, devname):
        if devname == "TIPI.STATUS" and mode(pab) == INPUT:
            if dataType(pab) == DISPLAY:
                if recordLength(pab) == 0 or recordLength(pab) == 80:
                    self.tipi_io.send([SUCCESS])
                    self.tipi_io.send([80])
                    self.tipiStatus = self.loadStatus()
                    self.recordNo = 0
                    return True
                else:
                    self.tipi_io.send([EOPATTR])
                    return True
        return False

    def loadStatus(self):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
	local_ip_address = s.getsockname()[0]
        return [ "ip={}".format(local_ip_address) ]

    def readStatus(self, pab, devname):
        if devname == "TIPI.STATUS" and mode(pab) == INPUT:
            if dataType(pab) == DISPLAY:
                readRec = recordNumber(pab)
                if readRec == 0:
                    readRec = self.recordNo
                else:
                    self.recordNo = readRec

                if readRec >= len(self.tipiStatus):
                    self.tipi_io.send([EEOF])
                    return True
                else:
		    fdata = bytearray(self.tipiStatus[readRec])
		    self.tipi_io.send([SUCCESS])
		    self.tipi_io.send(fdata)
		    self.recordNo += 1
		    return True
        return False



