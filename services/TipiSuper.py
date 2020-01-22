#!/usr/bin/env python2
#

import os
import sys
import time
from subprocess import call


def configureWifi(wificonfig):
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
        with open("/etc/wpa_supplicant/wpa_supplicant.conf",'w') as fh_out:
            with open("/home/tipi/tipi/services/templates/wpa_supplicant.conf") as fh_in:
                for line in fh_in:
                    line = line.replace("${SSID}", ssid)
                    line = line.replace("${PSK}", psk)
                    fh_out.write(line)

        # reload the new wpa_supplicant.conf
        callargs = ["/sbin/reboot", "now"]
        if call(callargs) != 0:
            raise Exception("failed to reload configuration")

    except Exception as e:
        print e

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
    elif os.path.exists("/tmp/tipireboot"):
        os.remove("/tmp/tipireboot")
        callargs = ["/sbin/shutdown", "-r", "now"]
        if call(callargs) != 0:
            raise Exception("failed to run /sbin/shutdown")
        else:
            while True:
                time.sleep(20)
                
    # Configure WiFi from TI-side
    elif os.path.exists("/tmp/wificonfig"):
        configureWifi("/tmp/wificonfig")
    
    # Configure WiFi from bootstrap file on USB stick:
    elif os.path.exists("/media/usb1/tipiwifi.txt"):
        configureWifi("/media/usb1/tipiwifi.txt")    

    # Upgrade TIPI services
    elif os.path.exists("/tmp/tipiupgrade"):
        os.remove("/tmp/tipiupgrade")
        callargs = ["/home/tipi/tipi/setup/upgrade.sh", "--upgrade"]
        if call(callargs) != 0:
            raise Exception("failed to run tipi upgrade")

    elif os.path.exists("/tmp/tz"):
        with open("/tmp/tz", 'r') as tz_file:
            timezone = tz_file.readline().rstrip()
        os.remove("/tmp/tz")
        callargs = ["/usr/bin/raspi-config", "nonint", "do_change_timezone", timezone]
        if call(callargs) != 0:
            raise Exception("failed to set timezone {}".format(timezone))


