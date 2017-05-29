
import time
import tipiports

tipiports.initGpio()

tipiports.setRD(255)
tipiports.setRC(0x55)

a = 1
while (a != 0):
    print "TC {} - TD {}".format(tipiports.getTC(), tipiports.getTD())

print a

