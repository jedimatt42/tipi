"""
Locations of TIPI's files.

On a Raspberry PI everything lives under /home/tipi. Set TIPI_HOME (and
TIPI_REPO, the checkout of this repository) to run the services elsewhere,
for example locally on a Mac in emulation mode (see emulation/local).
"""

import os

TIPI_HOME = os.environ.get("TIPI_HOME", "/home/tipi")
TIPI_REPO = os.environ.get("TIPI_REPO", os.path.join(TIPI_HOME, "tipi"))

TIPI_DISK = os.path.join(TIPI_HOME, "tipi_disk")
TIPI_CONFIG = os.path.join(TIPI_HOME, "tipi.config")
TIPI_UUID = os.path.join(TIPI_HOME, "tipi.uuid")
TIPI_LOG = os.path.join(TIPI_HOME, "log")
TIPI_VARS = os.path.join(TIPI_HOME, ".tipivars")
EMULATION_CONFIG = os.path.join(TIPI_HOME, ".emulation")
XDT99_DIR = os.environ.get("TIPI_XDT99", os.path.join(TIPI_HOME, "xdt99"))
# flag files and scratch files; the macOS app sandbox has its own temp folder
TIPI_TMP = os.environ.get("TIPI_TMP", "/tmp")
TIDBIT_DIR = os.path.join(TIPI_HOME, "tidbit")
