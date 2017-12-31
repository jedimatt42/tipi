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
	self.handlers = {
          0x12: self.handleProtect,
          0x13: self.handleFileRename,
          0x17: self.handleSetPath,
          0x18: self.handleCreateDir,
          0x19: self.handleDeleteDir,
          0x1A: self.handleDirRename
        }

    def handle(self, msg):
        handler = self.handlers.get(msg[0], self.defaultHandler)
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

        localname = self.getLocalName(unit,filename)

        try:
            bytes = self.getFileBytes(localname)
            ti_files.setProtected(bytes,protvalue)
            self.saveFile(localname,bytes)
            self.tipi_io.send([SUCCESS])
        except Exception as e:
            logger.error("Error setting protect bit", exc_info=True)
            self.tipi_io.send([EDEVERR])
        return True

    def handleFileRename(self):
        logger.debug("file rename request")
        unit = self.tipi_io.receive()[0]
        newfilename = str(self.tipi_io.receive()).strip()
        filename = str(self.tipi_io.receive()).strip()
        logger.debug("unit: %d, filename: %s, newname: %s", unit, filename, newfilename)

        origlocalname = self.getLocalName(unit,filename)
        newlocalname = self.getLocalName(unit,newfilename)

        if not os.path.exists(origlocalname):
            logger.debug("file doesn't exist: %s", origlocalname)
            self.tipi_io.send([EDEVERR])

        if os.path.exists(newlocalname):
            logger.debug("target file already exists: %s", newlocalname)
            self.tipi_io.send([EDEVERR])

        os.rename(origlocalname,newlocalname)
        logger.debug("file renamed to: %s", newlocalname)
        self.tipi_io.send([SUCCESS])
        return True

    def handleDirRename(self):
        logger.debug("dir rename request - delegating to file rename")
	return self.handleFileRename()

    def handleSetPath(self):
        logger.debug("set path request")
        unit = self.tipi_io.receive()[0]
        pathname = str(self.tipi_io.receive()).strip()
        logger.debug("unit: %d, path: %s", unit, pathname)
        self.unitpath[unit] = pathname
        self.tipi_io.send([SUCCESS])
        return True

    def handleCreateDir(self):
        logger.debug("create directory request")
        unit = self.tipi_io.receive()[0]
        dirname = str(self.tipi_io.receive()).strip()
        logger.debug("unit: %d, dir: %s", unit, dirname)
        localname = self.getLocalName(unit,dirname)
        try:
            os.makedirs(localname)
            self.tipi_io.send([SUCCESS])
        except Exception as e:
            logger.error("Error creating dir", exc_info=True)
            self.tipi_io.send([EDEVERR])
        return True
        
    def handleDeleteDir(self):
        logger.debug("delete directory request")
        unit = self.tipi_io.receive()[0]
        dirname = str(self.tipi_io.receive()).strip()
        logger.debug("unit: %d, dir: %s", unit, dirname)
        localname = self.getLocalName(unit,dirname)
        try:
            os.rmdir(localname)
            self.tipi_io.send([SUCCESS])
        except Exception as e:
            logger.error("Error deleting dir", exc_info=True)
            self.tipi_io.send([EDEVERR])
        return True
        
    def getLocalName(self,unit,filename):
        if self.unitpath[unit] != "":
            devname = self.unitpath[unit] + filename
        else:
            devname = "DSK" + str(unit) + "." + filename
        return tinames.devnameToLocal(devname)

    def getFileBytes(self,localname):
        with open(localname) as fh:
            bytes = bytearray(fh.read())
            if ti_files.isValid(bytes):
                return bytes
        return None
        
    def saveFile(self,localname,bytes):
        with open(localname,"wb") as fh:
            fh.write(bytes)

