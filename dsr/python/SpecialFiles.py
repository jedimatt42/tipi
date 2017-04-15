
from ClockFile import ClockFile
from StatusFile import StatusFile
from TcpFile import TcpFile

class SpecialFiles(object):

    def __init__(self, tipi_io):
        self.tipi_io = tipi_io
        self.specreg = { 
            ClockFile.filename(): ClockFile(self.tipi_io),
            StatusFile.filename(): StatusFile(self.tipi_io),
            TcpFile.filename(): TcpFile(self.tipi_io)
        }

    def handle(self, pab, devname):
        for prefix in self.specreg.keys():
            if devname.startswith(prefix):
                handler = self.specreg.get(prefix, None)
                handler.handle(pab, devname)
                return True
        return False

