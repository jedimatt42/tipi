import logging
import os
from ti_files import ti_files

# True if the file header indicates a matching file size if interpretted as a v9t9 file.
def isValid(filename):
    bytes = bytearray()
    with open(filename, "rb") as fh:
        bytes = fh.read()

    if len(bytes) < 128:
        return False

    tmpheader = bytearray(128)
    moveHeader(bytes, tmpheader)

    expectedlen = ti_files.getSectors(tmpheader) * 256
    flen = os.stat(filename).st_size
    if flen - 128 != expectedlen:
        return False
    return True


# Copy bytes from v9t9 header to position in TIFILES header
def moveHeader(vheader, theader):
    theader[8] = vheader[14]
    theader[9] = vheader[15]
    theader[10] = vheader[12]
    theader[11] = vheader[13]
    theader[12] = vheader[16]
    theader[13] = vheader[17]
    theader[14] = vheader[18]
    theader[15] = vheader[19]


# Safe v9t9 file as TIFILES file
def convert(filename):
    if not isValid(filename):
        return False

    bytes = bytearray(os.stat(filename).st_size)
    with open(filename, "rb") as fh:
        bytes = bytearray(fh.read())

    newheader = bytearray(128)
    newheader[0] = 7
    newheader[1:8] = bytearray("TIFILES")
    moveHeader(bytes, newheader)
    bytes[0:128] = newheader[0:128]

    with open(filename, "wb") as fh:
        fh.write(bytes)
        return True
