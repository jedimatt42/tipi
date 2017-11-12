#!/usr/bin/env python2
import os
import sys
import time
from subprocess import call

while True:
    time.sleep(1)

    # shutdown the PI safely
    if os.path.exists("/tmp/tipihalt"):
        os.remove("/tmp/tipihalt")
        callargs = ["/sbin/shutdown", "-h", "now"]
        if call(callargs) != 0:
            raise Exception("failed to run /sbin/shutdown")
        else:
            while True:
                time.sleep(20)
        
    # reboot the PI
    if os.path.exists("/tmp/tipireboot"):
        os.remove("/tmp/tipireboot")
        callargs = ["/sbin/shutdown", "-r", "now"]
        if call(callargs) != 0:
            raise Exception("failed to run /sbin/shutdown")
        else:
            while True:
                time.sleep(20)

    # Configure WiFi
    wificonfig="/tmp/wificonfig"
    if os.path.exists(wificonfig):
        # wait a couple seconds so file will be complete.
        time.sleep(2)
        # expect two config entries
        try:
            # read the username and password
            with open(wificonfig) as fh:
                ssid = fh.readline().rstrip()
                psk = fh.readline().rstrip()
            
            # remove handoff file
            os.remove(wificonfig)

            # adjust settings for network 0
            with open("/etc/wpa_supplicant/wpa_supplicant.conf", 'w') as fh_out:
                with open("/home/tipi/tipi/services/templates/wpa_supplicant.conf") as fh_in:
                    for line in fh_in:
                        line = line.replace("${SSID}", ssid)
                        line = line.replace("${PSK}", psk)
                        fh_out.write(line)

            # reload the new wpa_supplicant.conf
            callargs = ["/sbin/wpa_cli", "reconfigure"]
            if call(callargs) != 0:
                raise Exception("failed to reload configuration")

        except Exception as e:
            print e
        
