#!/usr/bin/env python
import sys
import time
from array import array

#
# Rev1 TIPI boards had the DSR ROM data lines backwards.
# This is not needed for Rev2 and up.
#
# I want to re-enable my Rev1 board, so I'm resurrecting this code.
#

fh = open("tipi.bin", 'rb')

with open("tipi.bin", 'rb') as fin:
    with open("tipi-reversed.bin", 'wb') as fout:
        bytes = bytearray(fin.read())
        for byte in bytes:
            fout.write(chr(int(bin(byte)[2:].zfill(8)[::-1], 2)))

