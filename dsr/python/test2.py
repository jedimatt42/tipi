#!/usr/bin/env python2

import sys
import time
from tipi.TipiPorts import TipiPorts
from tipi.TipiPorts import native

native = True
# native = False

tipiports = TipiPorts()

tipiports.setRC(0x50)
tipiports.setRD(0x0A)

a = 1
while (a != 0):
    tipiports.setRC(0x50)
    tipiports.setRD(0x0A)
    sys.stdout.write("native {} : TC {} - TD {}".format(native, tipiports.getTC(), tipiports.getTD()))
    sys.stdout.write('\r')

print a

