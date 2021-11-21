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

echo "restoring backup from $BACKUP"

tar -xvzf $BACKUP \
  -C /home/tipi \
  --owner=tipi \
  --one-file-system \

if [ -f ${WPATMP:-nofile} ]; then
  if [ "x${WPA:-no}" == "xyes" ]; then
    mv $WPATMP /boot/wpa_supplicant.conf
    rm $BACKUP
    reboot now
  else
    rm -f $WPATMP 
    rm -f /tmp/tipi_restore
  fi
fi



