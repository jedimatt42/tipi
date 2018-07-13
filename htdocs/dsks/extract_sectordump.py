import subprocess
import os
import sys
import traceback
import string
import pc99tov9t9

def rollDiskName(diskname):
    parts = diskname.split('_',2)
    last = parts[-1:][0]
    if last.isnumeric():
        parts[-1:] = [ str(1 + int(last)) ]
        return string.join(parts, '_')
    else:
        return diskname + "_1"

def getDiskName(diskfile, parentdir):
    diskname = 'unknown'
    listing = subprocess.check_output(['xdm99.py', diskfile, '-t', '--ti-names'], stderr=subprocess.STDOUT).decode('utf-8').split("\n")
    for line in listing:
        if 'free' in line:
            diskname = line.split(':')[0].strip()
            diskname = safename(diskname)
    dirname = parentdir + '/' + diskname
    while os.path.exists(dirname):
        diskname = rollDiskName(diskname)
        dirname = parentdir + '/' + diskname
    return diskname
   
def getFiles(diskfile):
    files = []
    listing = subprocess.check_output(['xdm99.py', diskfile, '-t', '--ti-names'], stderr=subprocess.STDOUT).decode('utf-8').split("\n")
    for line in listing:
        for key in ('PROGRAM', 'DIS/FIX', 'INT/FIX', 'DIS/VAR', 'INT/VAR'):
            if key in line:
                files.append(line.split(' ')[0])
    return files

def safename(n):
    s = n.replace('/', '.')
    s = s.replace('\\', '.')
    return s

def extractFile(diskfile, fname, diskname):
    newname = "%s/%s" % (diskname, safename(fname))
    subprocess.call(['xdm99.py', diskfile, '-t', '-e', fname, '-o', newname])

TMPFILE = '/tmp/sdump.dsk'

def extractDisk(diskfile):
    try:
        parentname = os.path.dirname(diskfile)
        sectorfile = diskfile
        if pc99tov9t9.dumpSectors(diskfile, TMPFILE):
            sectorfile = TMPFILE
        
        dirname = os.path.dirname(diskfile)
        diskname = getDiskName(sectorfile, dirname)
        dirname = parentname + '/' + diskname
        files = getFiles(sectorfile)
        os.mkdir(dirname)
        for f in files:
            extractFile(sectorfile, f, dirname)
        os.unlink(diskfile)
    except:
        print "failed to extract disk image: " + diskfile
        traceback.print_exc()
    if os.path.exists(TMPFILE):
        os.unlink(TMPFILE)

if __name__ == "__main__":
    extractDisk(sys.argv[1])
