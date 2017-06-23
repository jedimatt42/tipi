#!/usr/bin/env python2

import time
import logging
import logging.handlers
import tipiports
from tipi.TipiMessage import TipiMessage

LOG_FILENAME = "/var/log/tipi/tipi.log"
logging.getLogger('').setLevel(logging.DEBUG)
loghandler = logging.handlers.RotatingFileHandler(
                 LOG_FILENAME, maxBytes=(5000 * 1024), backupCount=5)
logformatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
loghandler.setFormatter(logformatter)
logging.getLogger('').addHandler(loghandler)

tipi_io = TipiMessage()

while True:
    buf = tipi_io.receive()
    tipi_io.send(buf)

