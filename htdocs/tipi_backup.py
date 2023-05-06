import glob
import os
import re
import time

from datetime import datetime

def get_archive_timestamp(filename):
    try:
        timestamp_str = re.sub('tipi-backup-', '', filename)
        timestamp_str = re.sub('[-+]\d+\.tar\.gz', '', timestamp_str)
        # now it should look like 2021-11-20T230628
        return datetime.strptime(timestamp_str, '%Y-%m-%dT%H%M%S')
    except Exception:
        return "unknown"


def restore_status():
    if os.path.exists("/tmp/restore_state"):
        with open("/tmp/restore_state", "r") as f:
            line = f.readline().strip()
        os.unlink("/tmp/restore_state")
        return line
    elif os.path.exists("/tmp/tipi_restore"):
        return "inprogress" 
    else:
        return "none"


def status():
    filelist = glob.glob("/home/tipi/*.tar.gz")
    filelist.sort()

    backups = [ {
            "name": os.path.basename(f),
            "date": get_archive_timestamp(os.path.basename(f)),
            "size": str(os.path.getsize(f)//1024) + "K",
            "dl_link": f"/backupdl/{os.path.basename(f)}"
        } for f in filelist ]

    status = { 
        "backups": backups,
        "backup_status": "inprogress" if os.path.exists("/tmp/tipi_backup") else "none",
        "restore_status": restore_status()
    }

    return status


def backup_now():
    with open("/tmp/tipi_backup", "w") as f:
        f.write("now")
    time.sleep(1)


def restore_now(backup_file):
    if backup_file is not None:
        with open("/tmp/tipi_restore", "w") as f:
            f.write(f"/home/tipi/{backup_file}")
        time.sleep(1)


def upload(fileset):
    for filedata in fileset:
        localfilename = os.path.join("/home/tipi", filedata.filename)
        filedata.save(localfilename)


def delete(backup_file):
    if backup_file is not None:
        fullpath = f"/home/tipi/{backup_file}"
        if os.path.exists(fullpath):
            os.remove(fullpath)

