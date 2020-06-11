import logging

logger = logging.getLogger(__name__)

#
# PAB routines...
#

OPEN = 0
CLOSE = 1
READ = 2
WRITE = 3
RESTORE = 4
LOAD = 5
SAVE = 6
DELETE = 7
SCRATCH = 8
STATUS = 9

#
# Return the TI DSR Opcode


def opcode(pab):
    return int(pab[0])


# Constants for fileType
SEQUENTIAL = 0x00
RELATIVE = 0x01


def fileType(pab):
    return pab[1] & 0x01


# Constants for modes
UPDATE = 0x00
OUTPUT = 0x01
INPUT = 0x02
APPEND = 0x03


def mode(pab):
    return (pab[1] & 0x06) >> 1


# Data types
DISPLAY = 0x00
INTERNAL = 0x01


def dataType(pab):
    return (pab[1] & 0x08) >> 3


# Record types
FIXED = 0x00
VARIABLE = 0x01


def recordType(pab):
    return (pab[1] & 0x10) >> 4


# Length of file records


def recordLength(pab):
    return pab[4]


#
# Return byte count from PAB / or byte count in LOAD/SAVE operations


def recordNumber(pab):
    return (pab[6] << 8) + pab[7]


#
# pretty pab string


def logPab(pab):
    opcodes = {
        0: "Open",
        1: "Close",
        2: "Read",
        3: "Write",
        4: "Restore",
        5: "Load",
        6: "Save",
        7: "Delete",
        8: "Scratch",
        9: "Status",
    }
    fileTypes = {SEQUENTIAL: "Sequential", RELATIVE: "Relative"}
    modes = {UPDATE: "Update", OUTPUT: "Output", INPUT: "Input", APPEND: "Append"}
    dataTypes = {DISPLAY: "Display", INTERNAL: "Internal"}
    recordTypes = {FIXED: "Fixed", VARIABLE: "Variable"}
    logger.info(
        "opcode: %s, fileType: %s, mode: %s, dataType: %s, recordType: %s, recordLength: %d, recordNumber: %d",
        opcodes[opcode(pab)],
        fileTypes[fileType(pab)],
        modes[mode(pab)],
        dataTypes[dataType(pab)],
        recordTypes[recordType(pab)],
        recordLength(pab),
        recordNumber(pab),
    )


#
# Error Codes
EDVNAME = 0x00
EWPROT = 0x01
EOPATTR = 0x02
EILLOP = 0x03
ENOSPAC = 0x04
EEOF = 0x05
EDEVERR = 0x06
EFILERR = 0x07
# TIPI Success
SUCCESS = 0xFF

#
# Status constants to be OR'ed together
STNOFILE = 0x80
STPROTECTED = 0x40
STRES1 = 0x20
STINTERNAL = 0x10
STPROGRAM = 0x08
STVARIABLE = 0x04
STPEOF = 0x02
STLEOF = 0x01
