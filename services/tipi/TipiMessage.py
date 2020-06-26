import time
import logging
from .TipiPorts import TipiPorts


class BackOffException(Exception):
    pass


logger = logging.getLogger(__name__)

class TipiMessage(object):
    def __init__(self):
        self.ports = TipiPorts.getInstance()

    #
    # Receive a message, returned as a byte array
    def receive(self):
        logger.debug("waiting to receive message...")
        startTime = time.time()
        message = self.ports.readMsg()
        if message == None:
            raise BackOffException('safepoint')
        elapsed = time.time() - startTime
        logger.debug(
            "received msg len %d, rate %d bytes/sec",
            len(message),
            len(message) / elapsed,
        )
        return message

    #
    # Send an array of data as is... no length prefix or hash
    def send(self, bytes):
        logger.debug("waiting to send message...")
        startTime = time.time()
        self.ports.sendMsg(bytes)
        elapsed = time.time() - startTime
        logger.debug(
            "sent msg len %d, rate %d bytes/sec", len(bytes), len(bytes) / elapsed
        )

    #
    # Trigger sending mouse event
    def sendMouseEvent(self):
        self.ports.sendMouseEvent()
