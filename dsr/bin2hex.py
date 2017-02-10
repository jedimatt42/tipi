#!/usr/bin/env python
import sys
import time
from array import array

fh = open("tipi.bin", 'rb')
try:
    bytes = bytearray(fh.read())
    for byte in bytes:
        print hex(byte)[2:].zfill(2)
finally:
    fh.close()
 
