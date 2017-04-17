import os
import traceback
import pycurl
from io import BytesIO

from Pab import *

class CurlFile(object):

    @staticmethod
    def filename():
        # open file in "input" for GET, "output" for POST
        #   TIPI.HTTP://ti994a.cwfk.net/tipi.html
        return "TIPI.HTTP:"

    def __init__(self, tipi_io):
        self.tipi_io = tipi_io
        self.bodies = { }
        self.record = { }

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
        print "close devname: {}".format(devname)
        self.tipi_io.send([SUCCESS])
        try:
            del(self.bodies[devname])
            del(self.record[devname])
        except:
            pass

    def open(self, pab, devname):
        print "open devname: {}".format(devname)
        try:
            url = self.parseDev(devname)
            print "fetching url: {}".format(url)
            buffer = BytesIO()
            c = pycurl.Curl()
            c.setopt(c.URL, url)
            c.setopt(c.WRITEDATA, buffer)
            c.perform()
            c.close()
            body = bytearray(buffer.getvalue())
            self.bodies[devname] = body
            self.record[devname] = 0
            print "body type: {}".format(type(body).__name__)
        except:
            self.tipi_io.send([EFILERR])
            return

        recLen = recordLength(pab)
        if recLen == 0:
            recLen = 80
        self.tipi_io.send([SUCCESS])
        self.tipi_io.send([recLen])
        return

    def read(self, pab, devname):
        print "read devname: {}".format(devname)
        try:
            body = self.bodies[devname]
            recLen = recordLength(pab)
            record = self.record[devname]
            lbody = len(body)
            startOff = record * recLen
            if startOff >= lbody:
               self.tipi_io.send([EEOF])
               return
            endOff = (record + 1) * recLen
            if endOff >= lbody:
                endOff = lbody
            fdata = body[startOff:endOff]
            print "sending rec {} - {}".format(record, fdata)
            self.tipi_io.send([SUCCESS])
            self.tipi_io.send(fdata)
            self.record[devname] = record + 1
            return
        except:
            traceback.print_exc()
        self.tipi_io.send([EEOF])
        return

    def parseDev(self, devname):
        return str(devname[5:])

