#!/usr/bin/env python

import sys
import time

from tipi.TipiMessage import TipiMessage

tipi_io = TipiMessage()

bytes = tipi_io.receive()

for byte in bytes:
  print '{0:0>2x} '.format(byte)
  sys.stdout.flush()

