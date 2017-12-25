import logging

from ClockFile import ClockFile
from StatusFile import StatusFile
from TcpFile import TcpFile
from CurlFile import CurlFile
from ConfigFile import ConfigFile
from UpgradeFile import UpgradeFile
from ShutdownFile import ShutdownFile
from RebootFile import RebootFile
from TipiConfig import TipiConfig

logger = logging.getLogger(__name__)

tipi_config = TipiConfig.instance()

class SpecialFiles(object):

    def __init__(self, tipi_io):
        self.tipi_io = tipi_io
        self.specreg = {
            TcpFile.filename(): TcpFile(self.tipi_io),
            ClockFile.filename(): ClockFile(self.tipi_io),
            StatusFile.filename(): StatusFile(self.tipi_io),
            CurlFile.filename(): CurlFile(self.tipi_io),
            ConfigFile.filename(): ConfigFile(self.tipi_io),
            UpgradeFile.filename(): UpgradeFile(self.tipi_io),
            RebootFile.filename(): RebootFile(self.tipi_io),
            ShutdownFile.filename(): ShutdownFile(self.tipi_io)
        }

    def handle(self, pab, devname):
        if devname.startswith("URI[1-3]".):
            uriShortcut = str(devname[:4])
            link = tipi_config.get(uriShortCut)
            if link != "":
                devname = "PI." + link + "/" + devname[5:]
                logger.debug("using %s to map to %s", uriShortcut, devname)
        if devname.startswith("PI."):
            fname = str(devname[3:])
            logger.debug("Looking for special file handler: %s", fname)
            for prefix in self.specreg.keys():
                if fname.startswith(prefix):
                    handler = self.specreg.get(prefix, None)
                    handler.handle(pab, devname)
                    return True
        return False
