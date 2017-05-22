
import time
import tipiports

tipiports.initGpio()

while True:
    tipiports.setRC(0x55)
    time.sleep(0.1)
    tipiports.setRD(0xAA)
    time.sleep(0.1)
    print tipiports.getTC()
    time.sleep(1)
    print tipiports.getTD()
    time.sleep(1)

# oldtc = -1

# while True:
#    time.sleep(0.1)
#    tc = tipiports.getTD()
#    if tc != oldtc:
#        print tc
#        oldtc = tc

