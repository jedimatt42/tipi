#!/bin/bash

id=`id -u`
if [ "x${id}" != "x0" ]; then
  echo "must run as root"
  exit 1
fi

if [ -f ${1:-nofile} ]; then
  BACKUP=$1
  WPA=yes
  shift
else
  if [ -f /tmp/tipi_restore ]; then
    BACKUP=`cat /tmp/tipi_restore`
  else
    echo "No backup to restore"
    exit 1
  fi
fi

WPATMP=/home/tipi/tmp_wpa_supplicant.conf

echo "stop conflicting services"
systemctl stop tipimon.service
systemctl stop tipi.service

echo "restoring backup from $BACKUP"

tar -xvzf $BACKUP \
  -C /home/tipi \
  --owner=tipi \
  --one-file-system \

if [ -f ${WPATMP:-nofile} ]; then
  if [ "x${WPA:-no}" == "xyes" ]; then
    mv $WPATMP /boot/wpa_supplicant.conf
    rm $BACKUP
    echo "rebooting..."
    reboot now
    sleep 10
  fi
fi

rm -f $WPATMP 
rm -f /tmp/tipi_restore
# If we don't reboot we should restart the services
echo "stop conflicting services"
systemctl restart tipimon.service
systemctl restart tipi.service



