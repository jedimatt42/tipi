import logging
from . import ti_files
from subprocess import call
from . import VariableRecordFile 

logger = logging.getLogger(__name__)


class BasicFile(object):
    def __init__(self, bytes):
        self.body = bytes

    @staticmethod
    def load(unix_file_name):
        logger.info("load %s", unix_file_name)
        fh = None
        source_file_name = unix_file_name
        if source_file_name.lower().endswith(".tb"):
            logger.info("converting with tidbit: %s", source_file_name)
            try:
                tmpfp = "/tmp/tidbit_tmp"
                BasicFile.tidbit(source_file_name, tmpfp)
                source_file_name = tmpfp
            except Exception as e:
                logger.error("Error reading file %s", unix_file_name)
                raise
        try:
            tmpfp = "/tmp/xbas_tmp"
            BasicFile.toBasic(source_file_name, tmpfp)
            fh = open(tmpfp, "rb")
            bytes = bytearray(fh.read())
            return BasicFile(bytes)
        except Exception as e:
            logger.error("Error reading file %s", source_file_name)
            raise
        finally:
            if fh != None:
                fh.close()

    @staticmethod
    def create(fdata):
        return BasicFile(fdata)

    def save(self, unix_file_name):
        if unix_file_name.lower().endswith(".tb"):
            logger.warn("saving PROGRAM to .tb files not permitted")
            raise Exception("saving PROGRAM to .tb files not permitted")

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
        try:
            dv80fp = "/tmp/dv80_bas_tmp"
            cmdargs = ["python3", "/home/tipi/xdt99/xdm99.py", "-P", fp, "-o", dv80fp]
            logger.info("issuing command: " + str(cmdargs))
            if call(cmdargs) == 0:
                fp = dv80fp
        except:
            logger.exception('not able to load dv80 records')

        cmdargs = ["python3", "/home/tipi/xdt99/xbas99.py", "-c", "-o", tmpfp, fp]
        logger.info("issuing command: " + str(cmdargs))
        if call(cmdargs) != 0:
            raise Exception("Invalid BASIC Source")

    @staticmethod
    def toText(tmpfp, fp):
        cmdargs = ["python3", "/home/tipi/xdt99/xbas99.py", "-d", "-o", fp, tmpfp]
        logger.info("issuing command: " + str(cmdargs))
        if call(cmdargs) != 0:
            raise Exception("Invalid BASIC Program")

    @staticmethod
    def tidbit(fp, tmpfp):
        try:
            dv80fp = "/tmp/dv80_tid_tmp"
            cmdargs = ["python3", "/home/tipi/xdt99/xdm99.py", "-P", fp, "-o", dv80fp]
            logger.info("issuing command: " + str(cmdargs))
            if call(cmdargs) == 0:
                fp = dv80fp
        except:
            logger.exception('not able to load dv80 records')

        cmdargs = ["php", "/home/tipi/tidbit/tidbit_cmd.php", fp, "100", "10", tmpfp]
        logger.info("issuing command: " + str(cmdargs))
        if call(cmdargs) != 0:
            raise Exception("Invalid Tidbit Source")
