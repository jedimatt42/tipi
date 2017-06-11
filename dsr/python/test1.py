#!/usr/bin/env python2

import time
import tipiports
from tipi.TipiMessage import TipiMessage

tipi_io = TipiMessage()

while True:
    buf = tipi_io.receive()
    tipi_io.send(buf)

