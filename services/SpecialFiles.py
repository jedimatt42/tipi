import logging

from ClockFile import ClockFile
from StatusFile import StatusFile
from TcpFile import TcpFile
from CurlFile import CurlFile
from ConfigFile import ConfigFile

logger = logging.getLogger(__name__)

class SpecialFiles(object):

    def __init__(self, tipi_io):
        self.tipi_io = tipi_io
        self.specreg = {
            TcpFile.filename(): TcpFile(self.tipi_io),
            ClockFile.filename(): ClockFile(self.tipi_io),
            StatusFile.filename(): StatusFile(self.tipi_io),
            CurlFile.filename(): CurlFile(self.tipi_io),
            ConfigFile.filename(): ConfigFile(self.tipi_io)
        }

    def handle(self, pab, devname):
        if devname.startswith("PI."):
            fname = str(devname[3:])
            logger.debug("Looking for special file handler: %s", fname)
            for prefix in self.specreg.keys():
                if fname.startswith(prefix):
                    handler = self.specreg.get(prefix, None)
                    handler.handle(pab, devname)
                    return True
        return False
