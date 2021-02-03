import logging

from ClockFile import ClockFile
from ConfigFile import ConfigFile
from CurlFile import CurlFile
from RebootFile import RebootFile
from ShutdownFile import ShutdownFile
from StatusFile import StatusFile
from TcpFile import TcpFile
from UdpFile import UdpFile
from TipiConfig import TipiConfig
from UpgradeFile import UpgradeFile
from VariablesFile import VariablesFile
from PioFile import PioFile

logger = logging.getLogger(__name__)

tipi_config = TipiConfig.instance()


class SpecialFiles(object):
    def __init__(self, tipi_io):
        self.tipi_io = tipi_io
        self.specreg = {
            ClockFile.filename(): ClockFile(self.tipi_io),
            ConfigFile.filename(): ConfigFile(self.tipi_io),
            CurlFile.filename(): CurlFile(self.tipi_io),
            PioFile.filename(): PioFile(self.tipi_io),
            RebootFile.filename(): RebootFile(self.tipi_io),
            ShutdownFile.filename(): ShutdownFile(self.tipi_io),
            StatusFile.filename(): StatusFile(self.tipi_io),
            TcpFile.filename(): TcpFile(self.tipi_io),
            UdpFile.filename(): UdpFile(self.tipi_io),
            UpgradeFile.filename(): UpgradeFile(self.tipi_io),
            VariablesFile.filename(): VariablesFile(self.tipi_io),
        }

    def handle(self, pab, devname):
        logger.debug("Matching special file handler for: %s", devname)
        if devname.startswith(("URI1.", "URI2.", "URI3.")):
            uriShortcut = devname[:4]
            link = tipi_config.get(uriShortcut)
            if link != "":
                devname = "PI." + link + "/" + devname[5:]
                logger.debug("using %s to map to %s", uriShortcut, devname)
        if devname.startswith("PI."):
            fname = devname[3:]
            logger.debug("Looking for special file handler: %s", fname)
            for prefix in self.specreg.keys():
                if fname.startswith(prefix):
                    handler = self.specreg.get(prefix, None)
                    handler.handle(pab, devname)
                    return True
        return False
