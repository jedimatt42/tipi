import subprocess
import os
import sys
import traceback
import string
import logging


logger = logging.getLogger(__name__)


# Yield successive n-sized
# chunks from l.
def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i : i + n]


def put_fm_9_sector(sdump, sdata, track, head, sectorno, totaltracks):
    start = (head * (totaltracks * 9 * 256)) + (track * (9 * 256)) + (sectorno * 256)
    sdump[start : start + 256] = sdata


def put_mfm_18_sector(sdump, sdata, track, head, sectorno, totaltracks):
    start = (head * (totaltracks * 18 * 256)) + (track * (18 * 256)) + (sectorno * 256)
    sdump[start : start + 256] = sdata


def put_mfm_16_sector(sdump, sdata, track, head, sectorno, totaltracks):
    start = (head * (totaltracks * 16 * 256)) + (track * (16 * 256)) + (sectorno * 256)
    sdump[start : start + 256] = sdata


# FM handling


def is_fm_9_track_dump(filepath):
    with open(filepath, "rb") as fh:
        data = bytearray(fh.read())
        if int(data[22]) == 0xFE:
            tracks = len(data) / 3253
            if tracks == 80:
                logger.info("FM DSSD 40")
            elif tracks == 160:
                logger.info("FM DSSD 80")
            elif tracks == 40:
                logger.info("FM SSSD 40")
            return True
        else:
            return False


def fm_9_sectors(trackdata):
    data = trackdata[16:-231]
    return list(divide_chunks(data, 334))


def dump_fm_9_sectors(filepath, outfile):
    with open(filepath, "rb") as fh:
        data = bytearray(fh.read())
        tracks = list(divide_chunks(data, 3253))
        totaltracks = len(tracks)
        sectordump = bytearray(9 * 2 * totaltracks * 256)
        for track in tracks:
            sectors = fm_9_sectors(track)
            for sector in sectors:
                track = sector[7]
                head = sector[8]
                sectorno = sector[9]
                logger.info(f"fm ths: {track}, {head}, {sectorno}")
                sdata = sector[31 : 31 + 256]
                put_fm_9_sector(sectordump, sdata, track, head, sectorno, totaltracks)
    with open(outfile, "wb") as fh:
        fh.write(sectordump)


# MFM handling

# 18 Sectors per track 

def is_mfm_18_track_dump(filepath):
    with open(filepath, "rb") as fh:
        data = bytearray(fh.read())
        if int(data[50]) == 0xA1 and int(data[53]) == 0xFE:
            return True
    return False


def mfm_18_sectors(trackdata):
    data = trackdata[40:-712]
    return list(divide_chunks(data, 340))


def dump_mfm_18_sectors(filepath, outfile):
    with open(filepath, "rb") as fh:
        data = bytearray(fh.read())
        tracks = list(divide_chunks(data, 6872))
        maxhead = 0
        maxtrack = 0
        maxsector = 0
                
        for track in tracks:
            sectors = mfm_18_sectors(track)
            for sector in sectors:
                maxtrack = max(maxtrack, sector[14])
                maxhead = max(maxhead, sector[15])
                maxsector = max(maxsector, sector[16])

        totaltracks = maxtrack + 1

        sectordump = bytearray((maxsector + 1) * (maxhead + 1) * totaltracks * 256)
        for track in tracks:
            sectors = mfm_18_sectors(track)
            for sector in sectors:
                track = sector[14]
                head = sector[15]
                sectorno = sector[16]
                sdata = sector[58 : 58 + 256]
                put_mfm_18_sector(sectordump, sdata, track, head, sectorno, totaltracks)
    with open(outfile, "wb") as fh:
        fh.write(sectordump)



# 16 Sectors per track 

def is_mfm_16_track_dump(filepath):
    with open(filepath, "rb") as fh:
        data = bytearray(fh.read())
        if int(data[50]) == 0xA1 and int(data[53]) == 0xFE:
            return True
    return False


def mfm_16_sectors(trackdata):
    data = trackdata[40:-712]
    return list(divide_chunks(data, 340))


def dump_mfm_16_sectors(filepath, outfile):
    with open(filepath, "rb") as fh:
        data = bytearray(fh.read())
        tracks = list(divide_chunks(data, 6872))
        maxhead = 0
        maxtrack = 0
        maxsector = 0
                
        for track in tracks:
            sectors = mfm_16_sectors(track)
            for sector in sectors:
                maxtrack = max(maxtrack, sector[14])
                maxhead = max(maxhead, sector[15])
                maxsector = max(maxsector, sector[16])

        totaltracks = maxtrack + 1

        sectordump = bytearray((maxsector + 1) * (maxhead + 1) * totaltracks * 256)
        for track in tracks:
            sectors = mfm_16_sectors(track)
            for sector in sectors:
                track = sector[14]
                head = sector[15]
                sectorno = sector[16]
                sdata = sector[58 : 58 + 256]
                put_mfm_16_sector(sectordump, sdata, track, head, sectorno, totaltracks)
    with open(outfile, "wb") as fh:
        fh.write(sectordump)


def is_track_dump(diskfile):
    return is_fm_9_track_dump(diskfile) or is_mfm_18_track_dump(diskfile) or is_mfm_16_track_dump(diskfile)


# If detected as a track dump file, will convert to a sector dump file,
# and return True.. Otherwise returns false.
#   infile: full or relative path to source track dump file
#  outfile: full or relative path to sector dump file to create.
def dump_sectors(infile, outfile):
    if is_fm_9_track_dump(infile):
        dump_fm_9_sectors(infile, outfile)
        return True
    elif is_mfm_18_track_dump(infile):
        dump_mfm_18_sectors(infile, outfile)
        return True
    elif is_mfm_16_track_dump(infile):
        dump_mfm_16_sectors(infile, outfile)
        return True
    return False


if __name__ == "__main__":
    infile = sys.argv[1]
    outfile = sys.argv[2]
    logger.info(f"converting: '{infile}' to '{outfile}'")
    if dump_sectors(infile, outfile):
        logger.info("done")
    else:
        logger.info("ERROR: not a track dump file")

