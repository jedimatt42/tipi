import os
import io
import sys
import traceback
import math
import logging
from ti_files import ti_files

logger = logging.getLogger(__name__)

class ProgramImageFile(ti_files):

    def __init__(self, bytes):
        self.header = bytes[:128]
        self.body = bytes[128:]

    @staticmethod
    def load(unix_file_name):
        fh = None
        try:
            fh = fopen(unix_file_name, "rb")
            bytes = fh.read()
            if ti_files.isValid(bytes) and ti_files.isProgram(bytes):
                return ProgramImageFile(bytes)
        except expression as identifier:
            logger.error("not a valid Program Image TIFILE %s", unix_file_name)
            return None
        finally:
            if fh != None:
                fh.close()

    @staticmethod
    def create(device_name, unix_file_name, body):
        nameParts = str(devname).split('.')
        tiname = nameParts[len(nameParts) - 1]

        header = ti_files.createHeader(ti_files.PROGRAM, tiname, bytes)
        fdata = bytearray(256 * (len(bytes) / 256 + 1) + 128)
        fdata[0:127] = header
        fdata[128:] = bytes
        return ProgramImageFile(bytes)

    def save(unix_file_name):
        fh = fopen(unix_file_name, "wb")
        fh.write(header)
        fh.write(body)
        fh.close()

    def getImage(self):
        return self.body

    def getImageSize(self):
        return len(self.body)