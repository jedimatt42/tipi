import sys
import os
import re
import logging
from crccheck.crc import Crc15
from TipiConfig import TipiConfig
from unidecode import unidecode

# Transform a name supplied by the 4A into our storage path

logger = logging.getLogger(__name__)

tipi_config = TipiConfig.instance()

TIPI_DIR = "/home/tipi/tipi_disk"


def __driveMapping(key):
    path = tipi_config.get(key)

    if path == "" or path is None:
        return None

    if path == ".":
        return TIPI_DIR

    path = "/".join([x.replace("/", ".") for x in path.split(".")])
    path = TIPI_DIR + "/" + path
    return path


def devnameToLocal(devname, prog=False):
    parts = str(devname).split(".")
    path = None
    startpart = 1
    if parts[0] == "TIPI":
        path = TIPI_DIR
    elif parts[0] == "DSK0":
        path = TIPI_DIR
    elif parts[0] in ("DSK1", "DSK2", "DSK3", "DSK4", "DSK5", "DSK6", "DSK7", "DSK8", "DSK9",):
        path = __driveMapping(f"{parts[0]}_DIR")
    elif parts[0] == "DSK":
        path = __scanForVolume(parts[1])
        startpart = 2
    elif parts[0] == "CS1":
        path = __cs1Mapping()

    if path == None or path == "":
        logger.debug("no path matched")
        return None

    # skip native file modes when finding linux path
    # ignore concept of native flags in web ui
    # if len(parts) > startpart and parts[startpart] in NATIVE_FLAGS:
    #     startpart = startpart + 1

    for part in parts[startpart:]:
        if part != "":
            logger.debug("matching path part: %s", part)
            if part == parts[-1]:
                path += "/" + findpath(path, part, prog=prog)
            else:
                path += "/" + findpath(path, part, dir=True)
            logger.debug("building path: %s", path)

    path = str(path).strip()
    logger.debug("%s -> %s", devname, path)

    return path


# Transform long host filename to 10 character TI filename
def asTiShortName(name):
    parts = name.split("/")
    lastpart = parts[len(parts) - 1]
    name = lastpart.replace('.', '/')
    return encodeName(name)


def encodeName(name):
    bytes = bytearray(name, 'utf-8')
    if len(bytes) == len(name) and len(name) <= 10:
        return name
    else:
        crc = Crc15.calc(bytearray(name, 'utf-8'))
        prefix = unidecode(name)[:6]
        shortname = f'{prefix}`{baseN(crc, 36)}'
        return shortname


def baseN(num, b, numerals="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    return ((num == 0) and numerals[0]) or (
        baseN(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b]
    )


# Use the context of actual files to transform TI file names to possibly
# long TI names


def findpath(path, part, prog=False, dir=False):
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
                filter(lambda x: asTiShortName(x) == part, os.listdir(path))
            )
            if candidates:
                return candidates[0]

    return part
