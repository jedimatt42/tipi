import os
import io
import sys
import traceback
import logging
from Pab import *
from ti_files.ti_files import ti_files
from TipiConfig import TipiConfig
from tinames import tinames
from Oled import oled

logger = logging.getLogger(__name__)
tipiConfig = TipiConfig.instance()

class LevelTwo(object):

    def __init__(self, tipi_io):
        self.tipi_io = tipi_io
        self.unitpath = {
          0: "",
          1: "",
          2: "",
          3: "",
          4: ""
        }
	self.handlers = {
          0x12: self.handleProtect,
          0x13: self.handleFileRename,
          0x14: self.handleDirectInput,
          0x15: self.handleDirectOutput,
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
        oled.info("lvl2 protect/%d: %s", unit, filename)

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
        oled.info("lvl2 rename/%d: %s", unit, filename)

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
        oled.info("lvl2 path:/%d: %s", unit, pathname)
        self.unitpath[unit] = pathname

        localname = self.getLocalName(unit,"")
        if not os.path.exists(localname):
            self.tipi_io.send([EDEVERR])
        else:
            self.tipi_io.send([SUCCESS])
        return True

    def handleCreateDir(self):
        logger.debug("create directory request")
        unit = self.tipi_io.receive()[0]
        dirname = str(self.tipi_io.receive()).strip()
        logger.debug("unit: %d, dir: %s", unit, dirname)
        oled.info("lvl2 mkdir:/%d: %s", unit, pathname)
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
        oled.info("lvl2 rmdir:/%d: %s", unit, dirname)
        localname = self.getLocalName(unit,dirname)
        try:
            os.rmdir(localname)
            self.tipi_io.send([SUCCESS])
        except Exception as e:
            logger.error("Error deleting dir", exc_info=True)
            self.tipi_io.send([EDEVERR])
        return True

    def handleDirectInput(self):
        logger.debug("direct input")
        bytes = self.tipi_io.receive()
        unit = bytes[0]
        blocks = bytes[1]
        filename = str(self.tipi_io.receive()).strip()
        bytes = self.tipi_io.receive()
        startblock = bytes[1] + (bytes[0] << 8)
        logger.debug("unit: %d, blocks: %d, filename: %s, startblock %d", unit, blocks, filename, startblock)
        oled.info("lvl2 read:/%d: %d %s", unit, startblock, filename)
        
        localfilename = self.getLocalName(unit,filename)
        if not os.path.exists(localfilename):
            logger.error("file doesn't exist")
            self.tipi_io.send([EDEVERR])
            return True

        fbytes = self.getFileBytes(localfilename)
        if fbytes is None:
            logger.error("not TIFILES")
            self.tipi_io.send([EDEVERR])
            return True

        bytestart = 128 + (startblock * 256)
        byteend = bytestart + (blocks * 256)
        total = len(fbytes)
        if blocks != 0 and (bytestart > total or byteend > total):
            logger.error("request exceeds file size")
            self.tipi_io.send([EDEVERR])
            return True
        logger.debug("Request is good!")
        self.tipi_io.send([SUCCESS])

	finfo = bytearray(8)
	if blocks == 0:
            startblock = ti_files.getSectors(fbytes)
            logger.debug("setting total sectors: %d", startblock)

        finfo[0] = startblock >> 8
        finfo[1] = startblock & 0xff
        finfo[2:] = fbytes[10:16]
        logger.debug("Sending finfo")
	self.tipi_io.send(finfo)

	# blocks is max blocks... we could read less, and 
        # have to adjust if we do.
        logger.debug("Sending adjusted block count")
        self.tipi_io.send([blocks & 0xFF])

	if blocks != 0:
            blockdata = fbytes[bytestart:byteend]
            logger.debug("Sending file data: %d bytes", len(blockdata))
            self.tipi_io.send(blockdata)

        return True

    def handleDirectOutput(self):
        logger.debug("direct output")
        bytes = self.tipi_io.receive()
        unit = bytes[0]
        blocks = bytes[1]
        filename = str(self.tipi_io.receive()).strip()
        bytes = self.tipi_io.receive()
        startblock = bytes[1] + (bytes[0] << 8)
        finfo = bytes[2:]
        
        logger.debug("unit: %d, blocks: %d, filename: %s, startblock %d", unit, blocks, filename, startblock)
        oled.info("lvl2 write:/%d: %d %s", unit, startblock, filename)

        localfilename = self.getLocalName(unit,filename)

        if os.path.exists(localfilename):
            fbytes = self.getFileBytes(localfilename)
        else:
            raw = bytearray(startblock * 256)
            header = ti_files.createHeader(0, filename, raw)
            fbytes = header + raw

	if blocks == 0:
            fbytes[10:16] = finfo
            self.saveFile(localfilename, fbytes)

        logger.debug("Accepting request")
        self.tipi_io.send([SUCCESS])

        if blocks == 0:
            return True

        blockdata = self.tipi_io.receive()
        startbyte = 128 + (startblock * 256)
        endbyte = startbyte + (blocks * 256)
        fbytes[startbyte:endbyte] = blockdata
        self.saveFile(localfilename, fbytes)

	self.tipi_io.send([SUCCESS])
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

