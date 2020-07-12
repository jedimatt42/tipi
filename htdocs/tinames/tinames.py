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
    path = path.replace(".", "/")
    if path != "":
        path = TIPI_DIR + "/" + path
    return path


def devnameToLocal(devname):
    parts = str(devname).split(".")
    path = ""
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
        path = TIPI_DIR

    if path == "":
        return None

    for part in parts[1:]:
        if part != "":
            logger.debug("matching path part: %s", part)
            path += "/" + findpath(path, part)
            logger.debug("building path: %s", path)

    path = str(path)

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
                filter(lambda x: asTiShortName(x) == part, os.listdir(path))
            )
            if candidates:
                return candidates[0]

    return part
