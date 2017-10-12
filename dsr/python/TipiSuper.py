#!/usr/bin/env python2
import os
import sys
import time
from subprocess import call

while True:
    time.sleep(1)
    if os.path.exists("/tmp/tipihalt"):
        callargs = ["/sbin/shutdown", "-h", "now"]
        if call(callargs) != 0:
            raise Exception("failed to run /sbin/shutdown")
        else:
            while True:
                time.sleep(2)
        
    if os.path.exists("/tmp/tipireboot"):
        callargs = ["/sbin/shutdown", "-r", "now"]
        if call(callargs) != 0:
            raise Exception("failed to run /sbin/shutdown")
        else:
            while True:
                time.sleep(2)
        
