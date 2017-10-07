import logging
from ti_files import ti_files
from subprocess import call

logger = logging.getLogger(__name__)

class BasicFile(object):

    def __init__(self, bytes):
        self.body = bytes

    @staticmethod
    def load(unix_file_name):
        fh = None
        try:
            tmpfp = "/tmp/xbas_tmp"
            BasicFile.toBasic(unix_file_name, tmpfp)
            fh = open(tmpfp, "rb")
            bytes = bytearray(fh.read())
            return BasicFile(bytes)
        except Exception as e:
            logger.error("Error reading file %s", unix_file_name)
            raise
        finally:
            if fh != None:
                fh.close()

    @staticmethod
    def create(fdata):
        return BasicFile(fdata)

    def save(self, unix_file_name):
        fh = None
        try:
            tmpfp = "/tmp/xbas_tmp"
            fh = open(tmpfp, "wb")
            fh.write(self.body)
            fh.close()
            fh = None
            BasicFile.toText(tmpfp, unix_file_name)
        except Exception as e:
            logger.exception("failed to save BasicFile")
            raise
        finally:
            if fh != None:
                fh.close()

    def getImage(self):
        return self.body

    def getImageSize(self):
        return len(self.body)

    @staticmethod
    def toBasic(fp, tmpfp):
        cmdargs = ["/home/tipi/xdt99/xbas99.py", "-c", "-o", tmpfp, fp]
        if call(cmdargs) != 0:
            raise Exception("Invalid BASIC Source")

    @staticmethod
    def toText(tmpfp, fp):
        cmdargs = ["/home/tipi/xdt99/xbas99.py", "-d", "-o", fp, tmpfp]
        if call(cmdargs) != 0:
            raise Exception("Invalid BASIC Program")
 
