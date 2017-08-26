#!/usr/bin/env python
import sys
import time
from array import array

fh = open("tipi.bin", 'rb')

try:
    bytes = bytearray(fh.read())
    for byte in bytes:
        sys.stdout.write(chr(int(bin(byte)[2:].zfill(8)[::-1], 2)))
finally:
    fh.close()

sys.stdout.flush()

