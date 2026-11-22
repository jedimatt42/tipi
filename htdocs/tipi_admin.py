# TIPI web administration
#
# Corey J. Anderson ElectricLab.com 2017
# et al.
import io
import subprocess
import os
from tipi_paths import TIPI_REPO, TIPI_LOG


def version():
    version = {}
    datafiles = [ "version.txt", "branch.txt" ]
    for f in datafiles:
        with open(os.path.join(TIPI_REPO, f)) as vt:
            for line in vt.readlines():
                parts = line.split("=")
                version[str(parts[0].strip().lower())] = str(parts[1].strip())
    return version


def logdata():
    with io.open(os.path.join(TIPI_LOG, "tipi.log"), mode="r", encoding="utf-8") as f:
        return {"logdata": f.read()}


def oslogdata():
    return {"logdata": subprocess.run(['journalctl', '--no-page', '-b'], stdout=subprocess.PIPE).stdout.decode('utf-8') }


def reboot():
    with open("/tmp/tipireboot", "w") as trigger:
        trigger.write("tipi")


def shutdown():
    with open("/tmp/tipihalt", "w") as trigger:
        trigger.write("tipi")


def upgrade():
    with open("/tmp/tipiupgrade", "w") as trigger:
        trigger.write("tipi")
