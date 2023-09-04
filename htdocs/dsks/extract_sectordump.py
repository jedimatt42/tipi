import subprocess
import os
import sys
import traceback
import string
from dsks import pc99tov9t9
import logging
import shutil


logger = logging.getLogger(__name__)


def rollDiskName(diskname):
    parts = diskname.split("_", 2)
    last = parts[-1:][0]
    if last.isnumeric():
        parts[-1:] = [str(1 + int(last))]
        return "_".join(parts)
    else:
        return diskname + "_1"


def getDiskName(diskfile, parentdir):
    diskname = "unknown"
    listing = (
        subprocess.check_output(
            ["python3", "/home/tipi/xdt99/xdm99.py", diskfile, "-t", "--ti-names"], stderr=subprocess.STDOUT
        )
        .decode("utf-8")
        .split("\n")
    )
    for line in listing:
        if "free" in line:
            diskname = line.split(":")[0].strip()
            diskname = safename(diskname)
    dirname = parentdir + "/" + diskname
    while os.path.exists(dirname):
        diskname = rollDiskName(diskname)
        dirname = parentdir + "/" + diskname
    return diskname


def getFiles(diskfile):
    files = []
    listing = (
        subprocess.check_output(
            ["python3", "/home/tipi/xdt99/xdm99.py", diskfile, "-t", "--ti-names"], stderr=subprocess.STDOUT
        )
        .decode("utf-8")
        .split("\n")
    )
    for line in listing:
        for key in ("PROGRAM", "DIS/FIX", "INT/FIX", "DIS/VAR", "INT/VAR"):
            if key in line:
                files.append(line.split(" ")[0])
    return files


def safename(n):
    s = n.replace("/", ".")
    s = s.replace("\\", ".")
    s = s.replace('\0', ' ').strip()
    return s


def extractFile(diskfile, fname, diskname):
    newname = "%s/%s" % (diskname, safename(fname))
    subprocess.call(["python3", "/home/tipi/xdt99/xdm99.py", diskfile, "-t", "-e", fname, "-o", newname])


TMPFILE = "/tmp/sdump.dsk"


def extractDisk(diskfile):
    try:
        parentname = os.path.dirname(diskfile)
        sectorfile = diskfile
        if pc99tov9t9.dump_sectors(diskfile, TMPFILE):
            sectorfile = TMPFILE

        dirname = os.path.dirname(diskfile)
        diskname = getDiskName(sectorfile, dirname)
        dirname = parentname + "/" + diskname
        files = getFiles(sectorfile)
        os.mkdir(dirname)
        for f in files:
            extractFile(sectorfile, f, dirname)
        # copy sector file to .sectors inside dir
        shutil.copy(sectorfile, f'{dirname}/.sectors')
        os.unlink(diskfile)
    except:
        logger.exception("failed to extract disk image: " + diskfile)
    if os.path.exists(TMPFILE):
        os.unlink(TMPFILE)


if __name__ == "__main__":
    extractDisk(sys.argv[1])
