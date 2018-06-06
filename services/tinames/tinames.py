import sys
import os
import re
import logging
from crccheck.crc import Crc15
from TipiConfig import TipiConfig

# Transform a name supplied by the 4A into our storage path

logger = logging.getLogger(__name__)

tipi_config = TipiConfig.instance()

TIPI_DIR = "/home/tipi/tipi_disk"

def __driveMapping(key):
    path = tipi_config.get(key)
    path = path.replace('.', "/")
    if path != "":
        path = TIPI_DIR + "/" + path
    return path

def __scanForVolume(volume):
    disks = ("DSK1_DIR","DSK2_DIR","DSK3_DIR")
    for disk in disks:
        path = __driveMapping(disk)
        if path.endswith("/" + volume):
            return path
    # None of the Disks are mapped to this volume...
    # fall back to top level directories
    path = os.path.join(TIPI_DIR, volume)
    if os.path.exists(path):
        return path
    return None

def devnameToLocal(devname):
    parts = str(devname).split('.')
    path = None
    startpart = 1
    if parts[0] == "TIPI":
        path = TIPI_DIR
    elif parts[0] == "DSK0":
        path = TIPI_DIR
    elif parts[0] == "WDS1":
        path = TIPI_DIR
    elif parts[0] == "DSK4":
        path = TIPI_DIR
    elif parts[0] == "DSK1":
        path = __driveMapping("DSK1_DIR")
    elif parts[0] == "DSK2":
        path = __driveMapping("DSK2_DIR")
    elif parts[0] == "DSK3":
        path = __driveMapping("DSK3_DIR")
    elif parts[0] == "DSK":
        path = __scanForVolume(parts[1])
        startpart = 2

    if path == None:
        return None

    for part in parts[startpart:]:
        if part != "":
            logger.debug("matching path part: %s", part)
            path += "/" + findpath(path, part)
            logger.debug("building path: %s", path)

    path = str(path)

    return path

# Transform long host filename to 10 character TI filename
def asTiShortName(name):
    parts = name.split('/')
    lastpart = parts[len(parts)-1]
    name = lastpart.replace('.', '/')
    if len(name) <= 10:
        return name
    else:
        crc = Crc15.calc(bytearray(name[6:]))
        shortname = "{}`{}".format(name[:6], baseN(crc, 36))
        return str(shortname)


def baseN(num, b, numerals="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    return ((num == 0) and numerals[0]) or (
        baseN(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])

# Use the context of actual files to transform TI file names to possibly
# long TI names


def findpath(path, part):
    part = part.replace("/", ".").replace("\\", ".")
    # if the file actually exists (or dir) then use literal name
    if os.path.exists(os.path.join(path, part)):
        return part
    else:
        # if it doesn't exist, and the part has a short name hash, then search
        # for a os match
        if re.match("^[^ ]{6}[`][0-9A-Z]{3}$", part):
            # Now we must find all the names in 'path' and see which one we
            # should load.
            candidates = list(
                filter(
                    lambda x: asTiShortName(x) == part,
                    os.listdir(path)))
            if candidates:
                return candidates[0]

    return part
