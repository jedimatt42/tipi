#!/usr/bin/env python3
import logging
import logging.handlers
import os
import time
import errno
import yaml
from tipi.TipiMessage import TipiMessage
from tipi.TipiMessage import BackOffException
from tipi.TipiMessage import SoftResetException
from SpecialFiles import SpecialFiles
from Pab import *
from RawExtensions import RawExtensions
from LevelTwo import LevelTwo
from TipiDisk import TipiDisk

#
# Setup logging
#
logpath = "/home/tipi/log"
if not os.path.isdir(logpath):
    os.makedirs(logpath)

LOG_FILENAME = logpath + "/tipi.log"
logging.getLogger("").setLevel(logging.INFO)

if os.path.exists("/home/tipi/tipi/services/loggers.yml"):
    with open("/home/tipi/tipi/services/loggers.yml", 'r') as stream:
        loggers_config = yaml.load(stream, Loader=yaml.FullLoader)
        for key in loggers_config.keys():
            logging.getLogger(key).setLevel(logging._nameToLevel.get(loggers_config.get(key)))


loghandler = logging.handlers.RotatingFileHandler(
    LOG_FILENAME, maxBytes=(1000 * 1024), backupCount=2
)
logformatter = logging.Formatter(
    "%(asctime)-15s %(name)-12s: %(levelname)-8s %(message)s"
)
loghandler.setFormatter(logformatter)
logging.getLogger("").addHandler(loghandler)

__name__ = "TipiService"

logger = logging.getLogger(__name__)

if os.environ.get('TIPI_WEBSOCK'):
    logger.info("websocket mode enabled")
else:
    logger.info("physical mode enabled")

##
# MAIN
##
try:
    tipi_io = TipiMessage()
    specialFiles = SpecialFiles(tipi_io)
    rawExtensions = RawExtensions(tipi_io)
    levelTwo = LevelTwo(tipi_io)
    tipiDisk = TipiDisk(tipi_io)

    while True:
        try:
            service_loop()
        except SoftResetException as reset:
            logger.info("soft reset received");

except Exception as e:
    logger.error("Unhandled exception in main", exc_info=True)



def service_loop():
    logger.info("TIPI Ready")
    while True:
        logger.debug("waiting for request...")
        msg = None
        try:
            msg = tipi_io.receive()
        except BackOffException:
            time.sleep(0.10)
            if os.path.exists("/tmp/tipi_safepoint"):
                logger.info("found /tmp/tipi_safepoint, restarting")
                os.remove("/tmp/tipi_safepoint")
                quit()
        if msg is None:
            continue

        if levelTwo.handle(msg):
            continue

        if rawExtensions.handle(msg):
            continue

        # if not already handled, assume this is a PAB
        pab = msg
        logger.debug("PAB received.")

        logger.debug("waiting for devicename...")
        devicename = tipi_io.receive()

        filename = str(devicename, 'latin1')
        if specialFiles.handle(pab, filename):
            continue

        # nothing special, so fall back to disk access
        tipiDisk.handle(pab, filename)

        logger.info("Request completed.")
