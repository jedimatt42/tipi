#!/usr/bin/env python

from TipiPorts import TipiPorts
from Phash import Phash

RESET = 0x01
TSWB = 0x02
TSRB = 0x06
ACK_MASK = 0x03

HASHOK = 0x5A
HASHERR = 0xA5

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
        print "waiting for reset..."
        # And wait for the TI to signal RESET
        self.prev_syn = 0
        while self.prev_syn != RESET:
            self.prev_syn = self.ports.getTC()
        # Reset the control signals
        self.ports.setRC(RESET)
        print "reset complete"

    #
    # change mode to sending bytes
    def __modeSend(self):
        # actual send calls will always pre-increment this, so we start a series by making sure the low bit will increment to zero.
        self.prev_syn = TSRB + 1

    #
    # transmit a byte when TI requests it
    def __sendByte(self, byte):
        next_syn = ((self.prev_syn + 1) & ACK_MASK) | TSRB
        while self.prev_syn != next_syn:
            self.prev_syn = self.ports.getTC()
        self.ports.setRD(byte)
        self.ports.setRC(self.prev_syn & ACK_MASK)
        print "Sent byte: >{0:x}".format(byte)

    #
    # change mode to sending bytes
    def __modeRead(self):
        # actual send calls will always pre-increment this, so we start a series by making sure the low bit will increment to zero.
        self.prev_syn = TSWB + 1

    #
    # block until byte is received.
    def __readByte(self):
        next_syn = ((self.prev_syn + 1) & ACK_MASK) | TSWB
        while self.prev_syn != next_syn:
            self.prev_syn = self.ports.getTC()
        next_ack = self.prev_syn
        val = self.ports.getTD()
        self.ports.setRC(self.prev_syn & ACK_MASK)
        #print 'received byte: {0:2x}'.format(val)
        return val

    #
    # exchange and check hash
    def __checkHash(self, bytes):
        hash = phash.digest(0, bytes)
        self.__sendByte(hash)
        self.__modeRead()
        return self.__readByte() == HASHOK

    #
    # Return an array of arrays
    def __splitMessage(self, bytes):
        l = len(bytes)
        chunks = [ ]
        bc = (l / 64) + 1
        for i in range(bc):
            chunk = bytes[i*64:(i+1)*64]
            chunks += [ chunk ]
        return chunks

        
    #
    # Receive a message, returned as a byte array
    def receive(self):
        self.__resetProtocol()
        self.__modeRead()
        msglen = (self.__readByte() << 8) + self.__readByte()
        message = bytearray(msglen)
        for i in range(0,msglen):
            message[i] = self.__readByte()
	return message

    #
    # Send a message, retrying each block if there is a transmission error.
    def send(self, bytes):
        self.__resetProtocol()
        self.__modeSend()
        msglen = len(bytes)
        msb = msglen >> 8
        lsb = msglen & 0xFF
        self.__sendByte(msb)
        self.__sendByte(lsb)
        for chunk in self.__splitMessage(bytes):
            clean = False
            while clean != True:
                for byte in chunk:
                    self.__sendByte(byte)
                clean = self.__checkHash(chunk)
                
