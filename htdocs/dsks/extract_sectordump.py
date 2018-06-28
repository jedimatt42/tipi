import subprocess
import os
import traceback

def getDiskName(diskfile):
    listing = subprocess.check_output(['xdm99.py', diskfile, '-t', '--ti-names'], stderr=subprocess.STDOUT).decode('utf-8').split("\n")
    for line in listing:
        if 'free' in line:
            return line.split(':')[0].strip()
    return 'unknown'
   
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

def extractDisk(diskfile):
    try:
        diskname = getDiskName(diskfile)
        dirname = os.path.dirname(diskfile) + '/' + diskname
        files = getFiles(diskfile)
        os.mkdir(dirname)
        for f in files:
            extractFile(diskfile, f, dirname)
        os.unlink(diskfile)
    except:
        print "failed to extract disk image: " + diskfile
        traceback.print_exc()

if __name__ == "__main__":
    extractDisk('TEST.DSK')

