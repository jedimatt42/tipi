import glob
import io
import os
import time


def status():
    filelist = glob.glob("/home/tipi/tipi-backup*.tar.gz")

    backups = [ {
            "name": os.path.basename(f),
            "date": time.strftime("%b %d %Y %H:%M:%S", time.gmtime(os.path.getmtime(f))),
            "dl_link": f"/backupdl/{os.path.basename(f)}"
        } for f in filelist ]

    status = { 
        "backups": backups,
        "backup_status": "inprogress" if os.path.exists("/tmp/tipi_backup") else "none",
        "restore_status": "inprogress" if os.path.exists("/tmp/tipi_restore") else "none"
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


