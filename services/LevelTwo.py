import os
import io
import sys
import traceback
import logging
from Pab import *
from ti_files.ti_files import ti_files
from TipiConfig import TipiConfig
from tinames import tinames

logger = logging.getLogger(__name__)
tipiConfig = TipiConfig.instance()

class LevelTwo(object):

    def __init__(self, tipi_io):
        self.tipi_io = tipi_io
        self.unitpath = {
          0: "",
          1: "",
          2: "",
          3: ""
        }
       

    def handle(self, msg):
	switcher = {
          0x12: self.handleProtect
        }
        handler = switcher.get(msg[0], self.defaultHandler)
        return handler()

    def defaultHandler(self):
        return False

    def handleProtect(self):
        logger.debug("protect request")
        bytes = self.tipi_io.receive()
        unit = bytes[0]
        protvalue = bytes[1]
        filename = str(self.tipi_io.receive()).strip()
        logger.debug("unit: %d, filename: %s, prot: %d", unit, filename, protvalue )

        devname = "DSK" + str(unit)
        if self.unitpath[unit] != "":
            devname = devname + "." + self.unitpath[unit]
        devname = devname + "." + filename
        localname = tinames.devnameToLocal(devname)

        try:
            bytes = self.getFileBytes(localname)
            ti_files.setProtected(bytes,protvalue)
            self.saveFile(localname,bytes)
            self.tipi_io.send([SUCCESS])
            return True
        except Exception as e:
            logger.error("Error setting protect bit", exc_info=True)
            self.tipi_io.send([EDEVERR])

    def getFileBytes(self,localname):
        with open(localname) as fh:
            bytes = bytearray(fh.read())
            if ti_files.isValid(bytes):
                return bytes
        return None
        
    def saveFile(self,localname,bytes):
        with open(localname,"wb") as fh:
            fh.write(bytes)

