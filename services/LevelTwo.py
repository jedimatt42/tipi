import os
import io
import sys
import traceback
import logging
from Pab import *
from ti_files import ti_files
from tinames import tinames
from TipiConfig import TipiConfig
from SectorDisk import SectorDisk


logger = logging.getLogger(__name__)
tipi_config = TipiConfig.instance()

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
          0x10: self.handleSector,
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

    def handleSector(self):
        logger.info("sector request")
        bytes = self.tipi_io.receive()
        unit = bytes[0]
        read_op = bytes[1] != 0
        bytes = self.tipi_io.receive()
        sector = bytes[1] + (bytes[0] << 8)
        logger.info("unit: %d, sector: %d, read: %d", unit, sector, read_op)
        disk_filename = self.getLocalDisk(unit)
        if not disk_filename:
            logger.info("no drive mapped for unit %d", unit)
            self.tipi_io.send([EDEVERR])
            return True
        if read_op:
            self.tipi_io.send([SUCCESS])
            data = SectorDisk.readSector(disk_filename, sector)
            self.tipi_io.send(data)
        else:
            # write op 
            self.tipi_io.send([SUCCESS])
            # get data from 4A
            sector_data = self.tipi_io.receive()
            SectorDisk.writeSector(disk_filename, sector, sector_data)
        return True

    def handleProtect(self):
        logger.info("protect request")
        bytes = self.tipi_io.receive()
        unit = bytes[0]
        protvalue = bytes[1]
        filename = str(self.tipi_io.receive(), 'latin1').strip()
        logger.info("unit: %d, filename: %s, prot: %d", unit, filename, protvalue )

        localfilename = self.getLocalName(unit,filename)
        if localfilename is None:
            logger.info("passing request to next device")
            self.tipi_io.send([EDVNAME])
            return True

        try:
            bytes = self.getFileBytes(localfilename)
            ti_files.setProtected(bytes,protvalue)
            self.saveFile(localfilename,bytes)
            self.tipi_io.send([SUCCESS])
        except Exception as e:
            logger.error("Error setting protect bit", exc_info=True)
            self.tipi_io.send([EDEVERR])
        return True

    def handleFileRename(self):
        logger.info("file rename request")
        unit = self.tipi_io.receive()[0]
        newfilename = str(self.tipi_io.receive(), 'latin1').strip()
        filename = str(self.tipi_io.receive(), 'latin1').strip()
        logger.info("unit: %d, filename: %s, newname: %s", unit, filename, newfilename)

        origlocalname = self.getLocalName(unit,filename)
        if origlocalname is None:
            logger.info("passing request to next device")
            self.tipi_io.send([EDVNAME])
            return True
        newlocalname = self.getLocalName(unit,newfilename)

        if not os.path.exists(origlocalname):
            logger.info("file doesn't exist: %s", origlocalname)
            self.tipi_io.send([EDEVERR])

        if os.path.exists(newlocalname):
            logger.info("target file already exists: %s", newlocalname)
            self.tipi_io.send([EDEVERR])

        if os.path.isdir(origlocalname):
            os.rename(origlocalname,newlocalname)
        else:
            bytes = self.getFileBytes(origlocalname)
            bytes = ti_files.setHeaderFilename(newfilename, bytes)
            self.saveFile(newlocalname, bytes)
            os.unlink(origlocalname)

        logger.info("file renamed to: %s", newlocalname)
        self.tipi_io.send([SUCCESS])
        return True

    def handleDirRename(self):
        logger.info("dir rename request - delegating to file rename")
        return self.handleFileRename()

    def handleSetPath(self):
        logger.info("set path request")
        unit = self.tipi_io.receive()[0]
        pathname = str(self.tipi_io.receive(), 'latin1').strip()
        logger.info("unit: %d, path: %s", unit, pathname)
        
        # test if device is mapped
        if unit:
            # only check unit greater than 0. TIPI is unit 0 and doesn't
            # get mapped
            mapped = tipi_config.get(f"DSK{unit}_DIR")
            if not mapped:
                logger.info("device not mapped")
                self.tipi_io.send([EDEVERR])
                return True

        target = tinames.devnameToLocal(pathname)
        if not (os.path.exists(target) and os.path.isdir(target)):
            logger.info("target %s does not exist", target)
            self.tipi_io.send([EDEVERR])
            return True

        self.unitpath[unit] = pathname
        logger.info("set unit %s path to %s", unit, pathname)
        self.tipi_io.send([SUCCESS])
        return True

    def handleCreateDir(self):
        logger.info("create directory request")
        unit = self.tipi_io.receive()[0]
        dirname = str(self.tipi_io.receive(), 'latin1').strip()
        logger.info("unit: %d, dir: %s", unit, dirname)
        localname = self.getLocalName(unit,dirname)
        if localname is None:
            logger.info("passing request to next device")
            self.tipi_io.send([EDVNAME])
            return True
        try:
            os.makedirs(localname)
            self.tipi_io.send([SUCCESS])
        except Exception as e:
            logger.error("Error creating dir", exc_info=True)
            self.tipi_io.send([EDEVERR])
        return True
        
    def handleDeleteDir(self):
        logger.info("delete directory request")
        unit = self.tipi_io.receive()[0]
        dirname = str(self.tipi_io.receive(), 'latin1').strip()
        logger.info("unit: %d, dir: %s", unit, dirname)
        localname = self.getLocalName(unit,dirname)
        if localname is None:
            logger.info("passing request to next device")
            self.tipi_io.send([EDVNAME])
            return True
        try:
            os.rmdir(localname)
            self.tipi_io.send([SUCCESS])
        except Exception as e:
            logger.error("Error deleting dir", exc_info=True)
            self.tipi_io.send([EDEVERR])
        return True

    def handleDirectInput(self):
        logger.info("direct input")
        bytes = self.tipi_io.receive()
        unit = bytes[0]
        blocks = bytes[1]
        filename = str(self.tipi_io.receive(), 'latin1').strip()
        bytes = self.tipi_io.receive()
        startblock = bytes[1] + (bytes[0] << 8)
        logger.info("unit: %d, blocks: %d, filename: %s, startblock %d", unit, blocks, filename, startblock)
        
        localfilename = self.getLocalName(unit,filename)
        if localfilename is None:
            logger.info("passing request to next device")
            self.tipi_io.send([EDVNAME])
            return True
        if not os.path.exists(localfilename):
            logger.error("file doesn't exist")
            self.tipi_io.send([EDEVERR])
            return True
        if os.path.isdir(localfilename):
            logger.error("cannot read blocks from a directory")
            self.tipi_io.send([EDEVERR])
            return True

        fbytes = self.getFileBytes(localfilename)
        if fbytes is None:
            logger.error("not TIFILES")
            self.tipi_io.send([EDEVERR])
            return True

        bytestart = 128 + (startblock * 256)
        byteend = bytestart + (blocks * 256)
        total = ((((len(fbytes)-128) / 256) + 1) * 256) + 128
        logger.debug("requested bytes total: %d, start: %d, end: %d", total, bytestart, byteend)

        if blocks != 0 and (bytestart >= total or byteend > total):
            logger.error("request exceeds file size: t: %d, s: %d, e: %d", total, bytestart, byteend)
            self.tipi_io.send([EDEVERR])
            return True

        self.tipi_io.send([SUCCESS])

        if blocks == 0:
            startblock = ti_files.getSectors(fbytes)
            logger.debug("setting total sectors: %d", startblock)

        finfo = bytearray(8)
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
        logger.info("direct output")
        bytes = self.tipi_io.receive()
        unit = bytes[0]
        blocks = bytes[1]
        filename = str(self.tipi_io.receive(), 'latin1').strip()
        bytes = self.tipi_io.receive()
        startblock = bytes[1] + (bytes[0] << 8)
        finfo = bytes[2:]
        
        logger.info("unit: %d, blocks: %d, filename: %s, startblock %d", unit, blocks, filename, startblock)

        localfilename = self.getLocalName(unit,filename)
        if localfilename is None:
            logger.info("passing request to next device")
            self.tipi_io.send([EDVNAME])
            return True
        if os.path.exists(localfilename) and os.path.isdir(localfilename):
            logger.info("folder with same name exists")
            self.tipi_io.send([EDEVERR])
            return True

        # check protect flag
        if os.path.exists(localfilename) and ti_files.isTiFile(localfilename):
            fh = open(localfilename, "rb")
            header = bytearray(fh.read())[:128]
            # if ti_files.isProtected(header):
            #     self.tipi_io.send([EWPROT])
            #     return True

        bytestart = 128 + (startblock * 256)
        byteend = bytestart + (blocks * 256)
        logger.debug("requested bytes start: %d, end: %d", bytestart, byteend)

        if os.path.exists(localfilename) and blocks != 0:
            fbytes = self.getFileBytes(localfilename)
        else:
            raw = bytearray(byteend - 128)
            header = ti_files.createHeader(0, filename, raw)
            logger.debug("header len %d, raw len %d", len(header), len(raw))
            fbytes = header + raw
            logger.debug("created file bytes: %d", len(fbytes))

        if blocks == 0:
            fbytes[10:16] = finfo[0:6]
            self.saveFile(localfilename, fbytes)

        if blocks != 0:
            logger.info("tifiles.getSectors: %d", ti_files.getSectors(fbytes))
            total = 128 + (256 * ti_files.getSectors(fbytes))
            if bytestart >= total or byteend > total:
                logger.error("request exceeds file size: t: %d, s: %d, e: %d", total, bytestart, byteend)
                self.tipi_io.send([EDEVERR])
                return True

        logger.info("Accepting request")
        self.tipi_io.send([SUCCESS])

        if blocks == 0:
            return True

        blockdata = self.tipi_io.receive()
        fbytes[bytestart:byteend] = blockdata
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
        with open(localname, 'rb') as fh:
            bytes = bytearray(fh.read())
            if ti_files.isValid(bytes):
                return bytes
        return None
        
    def saveFile(self,localname,bytes):
        logger.debug("saveFile len: %d", len(bytes))
        with open(localname,"wb") as fh:
            fh.write(bytes)

    def getLocalDisk(self,unit):
        devname = "DSK" + str(unit) + "."
        return tinames.devnameToLocal(devname)

