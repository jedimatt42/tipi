
from ClockFile import ClockFile
from StatusFile import StatusFile

class SpecialFiles(object):

    def __init__(self, tipi_io):
        self.tipi_io = tipi_io
        self.specreg = { 
            ClockFile.filename(): ClockFile(self.tipi_io),
            StatusFile.filename(): StatusFile(self.tipi_io)
        }

    def handle(self, pab, devname):
        handler = get(self.specreg, None)
        if handler == None:
            return False
        handler.handle(pab, devname)
        return True

