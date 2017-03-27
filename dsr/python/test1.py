#!/usr/bin/env python

import sys
import time

from tipi.TipiMessage import TipiMessage
from tipi.TipiPorts import TipiPorts

tipi_io = TipiMessage()
tipi_ports = TipiPorts()

start = time.time()

for i in range(0,8192):
    time.sleep(0.001)
    tipi_ports.setRD(0)
    time.sleep(0.001)
    tipi_ports.setRD(i)

stop = time.time()

print stop - start

