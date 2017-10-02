import sys
import os
import re
from crccheck.crc import Crc15

# Transform a name supplied by the 4A into our storage path


def devnameToLocal(devname):
    parts = str(devname).split('.')
    path = ""
    if parts[0] == "TIPI":
        path = "/home/tipi/tipi_disk"
    elif parts[0] == "DSK0":
        path = "/home/tipi/tipi_disk"
    elif parts[0] == "DSK1":
        path = "/home/tipi/tipi_disk/DSK1"
    elif parts[0] == "DSK2":
        path = "/home/tipi/tipi_disk/DSK2"
    elif parts[0] == "DSK3":
        path = "/home/tipi/tipi_disk/DSK3"
    elif parts[0] == "DSK":
        path = "/home/tipi/tipi_disk"

    for part in parts[1:]:
        if part != "":
            path += "/" + findpath(path, part)

    path = str(path)

    return path

# Transform long host filename to 10 character TI filename


def asTiShortName(name):
    name = name.replace('.', '/')
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
    # if the file actually exists (or dir) then use literal name
    if os.path.exists(str(os.path.join(path, part))):
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
        else:
            lpart = part.replace("/", ".").replace("\\", ".")
            if os.path.exists(str(os.path.join(path, lpart))):
                return lpart
    return part
