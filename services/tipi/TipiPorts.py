import sys
import os
import logging
import time

if os.getenv('TIPI_WEBSOCK', None):
  import tipiports_websocket as tipiports
else:
  import tipiports_chardev as tipiports

logger = logging.getLogger(__name__)


class TipiPorts(object):
    def __init__(self):
        tipiports.initGpio()
        logger.info("GPIO initialized.")

    # Send whole message
    def sendMsg(self, data):
        tipiports.sendMsg(data)

    # Receive whole message
    def readMsg(self):
        return tipiports.readMsg()

    # Send mouse event message
    def sendMouseEvent(self):
        return tipiports.sendMouseEvent()

    # Use this method to make sure we only
    @staticmethod
    def getInstance():
        return singleton


singleton = TipiPorts()
