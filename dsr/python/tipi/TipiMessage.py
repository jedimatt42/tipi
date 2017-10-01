import time
import logging
from TipiPorts import TipiPorts

RESET = 0xF1
TSWB = 0x02
TSRB = 0x06

BACKOFF_DELAY = 10000

logger = logging.getLogger(__name__)


class TipiMessage(object):

    def __init__(self):
        self.prev_syn = 0
        self.ports = TipiPorts.getInstance()

    #
    # Block until both sides show control bits reset
    # The TI resets first, and then RPi responds
    #
    def __resetProtocol(self):
        logger.info("waiting for handshake...")
        # And wait for the TI to signal RESET
        backoff = BACKOFF_DELAY
        self.prev_syn = 0
        while self.prev_syn != RESET:
            backoff -= 1
            if backoff < 1:
                backoff = 1
                time.sleep(0.01)
            self.prev_syn = self.ports.getTC()
        # Reset the control signals
        self.ports.setRC(RESET)
        logger.debug("reset protocol complete.")

    #
    # change mode to sending bytes
    def __modeSend(self):
        # actual send calls will always pre-increment this, so we start a
        # series by making sure the low bit will increment to zero.
        self.prev_syn = TSRB + 1

    #
    # transmit a byte when TI requests it
    def __sendByte(self, byte):
        next_syn = ((self.prev_syn + 1) & 0x01) | TSRB
        while self.prev_syn != next_syn:
            self.prev_syn = self.ports.getTC()
        self.ports.setRD(byte)
        self.ports.setRC(self.prev_syn)
        logger.debug("Sent byte: %d", byte)

    #
    # change mode to sending bytes
    def __modeRead(self):
        # actual send calls will always pre-increment this, so we start a
        # series by making sure the low bit will increment to zero.
        self.prev_syn = TSWB + 1

    #
    # block until byte is received.
    def __readByte(self):
        next_syn = ((self.prev_syn + 1) & 0x01) | TSWB
        while self.prev_syn != next_syn:
            self.prev_syn = self.ports.getTC()
        next_ack = self.prev_syn
        val = self.ports.getTD()
        self.ports.setRC(self.prev_syn)
        logger.debug('received byte: %d', val)
        return val

    #
    # Receive a message, returned as a byte array
    def receive(self):
        self.__resetProtocol()
        startTime = time.time()
        self.__modeRead()
        msglen = (self.__readByte() << 8) + self.__readByte()
        logger.debug("msglen: %d", msglen)
        message = bytearray(msglen)
        for i in range(0, msglen):
            message[i] = self.__readByte()
        elapsed = time.time() - startTime
        logger.info(
            'received msg len %d, rate %d bytes/sec',
            len(message),
            len(message) / elapsed)
        return message

    #
    # Send an array of data as is... no length prefix or hash
    def send(self, bytes):
        startTime = time.time()
        self.__resetProtocol()
        self.__modeSend()
        msglen = len(bytes)
        msb = msglen >> 8
        lsb = msglen & 0xFF
        self.__sendByte(msb)
        self.__sendByte(lsb)
        for byte in bytes:
            self.__sendByte(byte)
        elapsed = time.time() - startTime
        logger.info(
            'sent msg len %d, rate %d bytes/sec',
            len(bytes),
            len(bytes) / elapsed)
