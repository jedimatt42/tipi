#!/bin/sh

# Things here run as root on system boot to make way for 
# standard boot services.

# /var/log is a tmpfs, need to add permissions on each boot
if [ ! -e /var/log/tipi ]; then
  mkdir /var/log/tipi
  chown tipi.tipi /var/log/tipi
fi

if [ ! -e /home/tipi/log ]; then
  ln -s /var/log/tipi /home/tipi/log
fi

if [ ! -e /home/tipi/tipi.uuid ]; then
( echo "import uuid" ; echo "print(uuid.uuid1())" ) | \
    python3 - >/home/tipi/tipi.uuid
fi

if [ -e /home/tipi/.emulation ]; then
  # mount nfs from host OS
  HOSTIP=`ip route | grep default | cut -d' ' -f3`
  mount -t nfs ${HOSTIP}:/tipi_disk /home/tipi/tipi_disk
else
  # disable power management for the wifi
  iwconfig wlan0 power off
fi


cp -R -a /home/tipi/tipi/setup/bin/* /home/tipi/tipi_disk/

