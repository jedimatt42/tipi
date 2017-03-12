#!/usr/bin/env python

from TipiPorts import TipiPorts

RESET = 0x01
TSWB = 0x02
TSRB = 0x06
ACK_MASK = 0x03

class TipiMessage(object):

    def __init__(self):
        self.prev_syn = 0
        self.ports = TipiPorts()

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
    # Receive a message, returned as a byte array
    def receive(self):
        self.__resetProtocol()
        self.__modeRead()
        msglen = (self.__readByte() << 8) + self.__readByte()
        message = bytearray(msglen)
        for i in range(0,msglen):
            message[i] = self.__readByte()
	return message


