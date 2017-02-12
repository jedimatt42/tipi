#!/usr/bin/env python
import sys
import time
from array import array

count = 0
fh = open("tipi.bin", 'rb')
try:
    bytes = bytearray(fh.read())
    for byte in bytes:
        print hex(byte)[2:].zfill(2)
        count += 1
finally:
    fh.close()

while count < 8192:
    print hex(0)[2:].zfill(2)
    count += 1

