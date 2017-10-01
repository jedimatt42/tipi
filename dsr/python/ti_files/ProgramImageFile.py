import logging
from ti_files import ti_files

logger = logging.getLogger(__name__)

class ProgramImageFile(object):

    def __init__(self, bytes):
        self.header = bytes[:128]
        self.body = bytes[128:]

    def isValid(self):
        return ti_files.isValid(self.header) and ti_files.isProgram(self.header)

    @staticmethod
    def load(unix_file_name):
        fh = None
        try:
            fh = open(unix_file_name, "rb")
            bytes = bytearray(fh.read())
            prog_file = ProgramImageFile(bytes)
            if prog_file.isValid():
                return prog_file
            else:
                raise Exception("Invalid Program Image")
        except Exception as e:
            logger.error("Error reading file %s", unix_file_name)
            raise
        finally:
            if fh != None:
                fh.close()

    @staticmethod
    def create(device_name, unix_file_name, body):
        nameParts = str(device_name).split('.')
        tiname = nameParts[len(nameParts) - 1]

        header = ti_files.createHeader(ti_files.PROGRAM, tiname, body)
        fdata = bytearray(256 * (len(body) / 256 + 1) + 128)
        fdata[0:127] = header
        fdata[128:] = body
        return ProgramImageFile(fdata)

    def save(self, unix_file_name):
        fh = open(unix_file_name, "wb")
        fh.write(self.header)
        fh.write(self.body)
        fh.close()

    def getImage(self):
        return self.body

    def getImageSize(self):
        return len(self.body)