import os
import logging
import time
import hashlib
import glob
from subprocess import call


logger = logging.getLogger(__name__)


class SectorDisk(object):

    @staticmethod
    def readSector(dir_name, sector):
        sector_file = SectorDisk.getSectorFile(dir_name)
        with open(sector_file, 'rb') as sector_file:
            b = 256 * sector
            return bytearray(sector_file.read()[b:b+256])

    @staticmethod
    def writeSector(dir_name, sector, sector_data):
        sector_file = SectorDisk.getSectorFile(dir_name)
        with open(sector_file, 'rb+') as sector_file:
            b = 256 * sector
            sector_file.seek(b)
            sector_file.write(sector_data)

    @staticmethod
    def hashPathName(dir_name):
        h = hashlib.sha256()
        # unix filesystem names are utf8
        h.update(bytearray(dir_name, 'utf8'))
        digest = h.hexdigest()
        return f'/tmp/{digest}.img'

    @staticmethod
    def createImage(dir_name, cache_name):
        try:
            cmdargs = ["bash", "/home/tipi/tipi/services/create_sectors.sh", cache_name, dir_name]
            logger.info("issuing command: " + str(cmdargs))
            if call(cmdargs) == 0:
                return
        except:
            logger.exception('not create disk image cache')

    @staticmethod
    def outdatedImage(dir_name, cache_name):
        files = glob.glob(f'{dir_name}/*')
        if files:
            max_file = max(files, key=os.path.getmtime)
            return os.path.getmtime(cache_name) < os.path.getmtime(max_file)
        else:
            return False

    @staticmethod
    def getSectorFile(dir_name):
        dot_sectors = f'{dir_name}/.sectors'
        if os.path.exists(dot_sectors):
            return dot_sectors

        cache_name = SectorDisk.hashPathName(dir_name)
        if not os.path.exists(cache_name):
            SectorDisk.createImage(dir_name, cache_name)
        else:
            if SectorDisk.outdatedImage(dir_name, cache_name):
                SectorDisk.createImage(dir_name, cache_name)
        return cache_name

