#!/usr/bin/env python
import sys
import time
from array import array

fh = open("tipi.bin", 'rb')
romSize = 8192

# Weird bug work-around... not long term. need to fix verilog code
while romSize > 7680:
    romSize -= 1
    print hex(0xFF)[2:].zfill(2)

try:
    bytes = bytearray(fh.read())
    for byte in bytes:
        print hex(byte)[2:].zfill(2)
        romSize -= 1
finally:
    fh.close()

while romSize > 0:
    romSize -= 1
    print hex(romSize >> 8 % 255)[2:].zfill(2)

