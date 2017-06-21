#!/usr/bin/env python

import time
import logging
from TipiPorts import TipiPorts
from Phash import Phash

RESET = 0xF1
TSWB = 0x02
TSRB = 0x06

HASHOK = 0x5A
HASHERR = 0xA5

CHUNKSIZE = 64

BACKOFF_DELAY = 10000

logger = logging.getLogger("tipi")

class TipiMessage(object):

    def __init__(self):
        self.prev_syn = 0
        self.ports = TipiPorts()
        self.phash = Phash()

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
        print "reset protocol complete."

    #
    # change mode to sending bytes
    def __modeSend(self):
        # actual send calls will always pre-increment this, so we start a series by making sure the low bit will increment to zero.
        self.prev_syn = TSRB + 1

    #
    # transmit a byte when TI requests it
    def __sendByte(self, byte):
        next_syn = ((self.prev_syn + 1) & 0x01) | TSRB
        while self.prev_syn != next_syn:
            self.prev_syn = self.ports.getTC()
        self.ports.setRD(byte)
        self.ports.setRC(self.prev_syn)
        print "Sent byte: >{0:2x}".format(byte)

    #
    # change mode to sending bytes
    def __modeRead(self):
        # actual send calls will always pre-increment this, so we start a series by making sure the low bit will increment to zero.
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
        print 'received byte: {0:2x}'.format(val)
        return val

    #
    # exchange and check hash
    def __checkHash(self, bytes):
        hash = self.phash.digestAll(0, bytes)
        self.__sendByte(hash)
        self.__modeRead()
        check = self.__readByte()
        self.__modeRead()
        return check == HASHOK

    #
    # Return an array of arrays
    def __splitMessage(self, bytes):
        l = len(bytes)
        chunks = [ ]
        bc = (l / CHUNKSIZE) + 1
        for i in range(bc):
            chunk = bytes[i*CHUNKSIZE:(i+1)*CHUNKSIZE]
            if len(chunk):
                chunks += [ chunk ]
        return chunks

        
    #
    # Receive a message, returned as a byte array
    def receive(self):
        self.__resetProtocol()
        startTime = time.time()
        self.__modeRead()
        msglen = (self.__readByte() << 8) + self.__readByte()
        print msglen
        message = bytearray(msglen)
        for i in range(0,msglen):
            message[i] = self.__readByte()
        elapsed = time.time() - startTime
        logger.info('received msg len %d, rate %d', len(message), len(message) / elapsed)
        return message

    #
    # Send a message, retrying each block if there is a transmission error.
    def send(self, bytes):
        self.__resetProtocol()
        startTime = time.time()
        self.__modeSend()
        msglen = len(bytes)
        msb = msglen >> 8
        lsb = msglen & 0xFF
        self.__sendByte(msb)
        self.__sendByte(lsb)
        cidx = 0
        retries = 0
        for chunk in self.__splitMessage(bytes):
            clean = False
            while clean != True:
                for byte in chunk:
                    self.__sendByte(byte)
                clean = self.__checkHash(chunk)
                if not clean:
                    retries += 1
            cidx += 1    
        elapsed = time.time() - startTime
        logger.info('send msg len %d, rate %d', len(bytes), len(bytes) / elapsed)
        if retries > 0:
            logger.info("message required %d retries", retries)

    #
    # Send an array of data as is... no length prefix or hash
    def sendRaw(self, bytes):
        self.__resetProtocol()
        self.__modeSend()
        for byte in bytes:
            self.__sendByte(byte)


