#!/usr/bin/env python2
import logging
import logging.handlers
import os
import errno
from tipi.TipiMessage import TipiMessage
from SpecialFiles import SpecialFiles
from Pab import *
from RawExtensions import RawExtensions
from ResetHandler import createResetListener
from TipiDisk import TipiDisk

#
# Setup logging
#
logpath = "/var/log/tipi"
try:
    os.makedirs(logpath)
except OSError as exc:
    if exc.errno == errno.EEXIST and os.path.isdir(logpath):
        pass
    else: raise

LOG_FILENAME = "/var/log/tipi/tipi.log"
logging.getLogger('').setLevel(logging.INFO)
loghandler = logging.handlers.RotatingFileHandler(
                 LOG_FILENAME, maxBytes=(5000 * 1024), backupCount=5)
logformatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
loghandler.setFormatter(logformatter)
logging.getLogger('').addHandler(loghandler)

logger = logging.getLogger('tipi')
oled = logging.getLogger('oled')

## 
## MAIN
##

oled.info("TIPI Init")

createResetListener()

tipi_io = TipiMessage()
specialFiles = SpecialFiles(tipi_io)
rawExtensions = RawExtensions(tipi_io)
tipiDisk = TipiDisk(tipi_io)

oled.info("TIPI Ready")

while True:
    logger.info("waiting for PAB request...")

    pab = tipi_io.receive()
    if rawExtensions.handle(pab):
        continue

    logger.debug("PAB received.")

    logger.debug("waiting for devicename...")
    devicename = tipi_io.receive()

    # Special file name requests to force different errors
    filename = str(devicename)

    if specialFiles.handle(pab, filename):
        continue

    # nothing special, so fall back to disk access
    tipiDisk.handle(pab, filename)

    logger.info("Request completed.")


