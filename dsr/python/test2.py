
import time
from tipi.TipiPorts import TipiPorts
from tipi.TipiPorts import native

native = True

tipiports = TipiPorts()

tipiports.setRD(0x01)
tipiports.setRC(0x80)

a = 1
while (a != 0):
    tipiports.setRD(0x01)
    tipiports.setRC(0x55)
    print "native {} : TC {} - TD {}".format(native, tipiports.getTC(), tipiports.getTD())

print a

