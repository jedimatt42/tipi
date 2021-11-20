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
        "status": "inprogress"
    }

    return status

