import logging

logger = logging.getLogger(__name__)

GOOD = bytearray([255])

class UserLog(object):
    def __init__(self, tipi_io):
        self.tipi_io = tipi_io

    def handle(self, bytes):
        self.tipi_io.send(self.processRequest(bytes))
        return True

    def processRequest(self, bytes):
        logger.info(str(bytes[1:], 'latin1'))
        return GOOD

