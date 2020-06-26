import struct
import fcntl
import os
import logging

logger = logging.getLogger(__name__)


class Mouse(object):
    def __init__(self, tipi_io):
        self.tipi_io = tipi_io

    def handle(self, bytes):
        self.tipi_io.sendMouseEvent()
        return True

