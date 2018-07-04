import subprocess
import os
import traceback
import string

# Yield successive n-sized
# chunks from l.
def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]

# need to determine track count instead of assuming 40
def putSector(sdump, sdata, track, head, sectorno):
    start = (head * (40 * 9 * 256)) + (track * (9 * 256)) + (sectorno * 256)
    sdump[start:start+256] = sdata

# FM handling

def isFmTrackDump(filepath):
    with open(filepath, 'rb') as fh:
        data = bytearray(fh.read())
        if int(data[22]) == 0xFE:
            tracks = len(data) / 3253
            if tracks == 80:
                print "FM DSSD 40"
            elif tracks == 160:
                print "FM DSSD 80"
            elif tracks == 40:
                print "FM SSSD 40"
            return True
        else:
            return False

def fm_sectors(trackdata):
    data = trackdata[16:-231]
    return list(divide_chunks(data, 334))

def dumpFmSectors(filepath, outfile):
    with open(filepath, 'rb') as fh:
        data = bytearray(fh.read())
        tracks = list(divide_chunks(data, 3253))
        sectordump = bytearray(9 * 2 * len(tracks) * 256)
        for track in tracks:
            sectors = fm_sectors(track)
            for sector in sectors:
                track = sector[7]
                head = sector[8]
                sectorno = sector[9]
                sdata = sector[31:31+256]
                putSector(sectordump, sdata, track, head, sectorno)
    with open(outfile, 'wb') as fh:
        fh.write(sectordump)

# MFM handling

def isMfmTrackDump(filepath):
    with open(filepath, 'rb') as fh:
        data = bytearray(fh.read())
        if int(data[50]) == 0xA1 and int(data[53]) == 0xFE:
            return True
    return False

def mfm_sectors(trackdata):
    data = trackdata[40:-712]
    return list(divide_chunks(data, 340))

def dumpMfmSectors(filepath, outfile):
    with open(filepath, 'rb') as fh:
        data = bytearray(fh.read())
        tracks = list(divide_chunks(data, 6872))
        sectordump = bytearray(18 * 2 * len(tracks) * 256)
        for track in tracks:
            sectors = mfm_sectors(track)
            for sector in sectors:
                track = sector[14]
                head = sector[15]
                sectorno = sector[16]
                print "ths: %d, %d, %d" % (track, head, sectorno)
                sdata = sector[58:58+256]
                putSector(sectordump, sdata, track, head, sectorno)
    with open(outfile, 'wb') as fh:
        fh.write(sectordump)

def isTrackDump(diskfile):
    return isFmTrackDump(diskfile) or isMfmTrackDump(diskfile)

# If detected as a track dump file, will convert to a sector dump file,
# and return True.. Otherwise returns false.
#   infile: full or relative path to source track dump file
#  outfile: full or relative path to sector dump file to create.
def dumpSectors(infile, outfile):
    if isFmTrackDump(infile):
        dumpFmSectors(infile, outfile)
        return True
    elif isMfmTrackDump(infile):
        dumpMfmSectors(infile, outfile)
        return True
    return False


