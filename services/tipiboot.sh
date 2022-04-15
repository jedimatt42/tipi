#!/bin/sh

SCRIPT_DIR=$(dirname $0)
TIPI_DIR=$(cd $SCRIPT_DIR/..; pwd)

source $TIPI_DIR/setup/tipi_paths.sh

cd $TIPI_DIR/services

# Things here run as root on system boot to make way for 
# standard boot services.

# Check /boot for a backup file
BACKUP=`ls -1 /boot/tipi-backup-*.tar.gz 2>/dev/null`
if [ -f ${BACKUP:-notfile} ]; then
  $TIPI_DIR/setup/restore.sh $BACKUP
fi

# /var/log is a tmpfs, need to add permissions on each boot
if [ ! -e /var/log/tipi ]; then
  mkdir /var/log/tipi
  chown tipi.tipi /var/log/tipi
fi

if [ ! -e $TIPI_CONF/log ]; then
  ln -s /var/log/tipi $TIPI_CONF/log
fi

if [ ! -e $TIPI_CONF/tipi.uuid ]; then
( echo "import uuid" ; echo "print(uuid.uuid1())" ) | \
    python3 - >$TIPI_CONF/tipi.uuid
fi

if [ -e $TIPI_CONF/.emulation ]; then
  grep "NFS_ENABLED=1" $TIPI_CONF/.emulation >/dev/null
  if [ $? = 0 ]; then
    # mount nfs from host OS
    HOSTIP=`ip route | grep default | cut -d' ' -f3`
    mount -t nfs ${HOSTIP}:/tipi_disk $TIPI_DISK
  fi
fi

# disable power management for the wifi
iwconfig wlan0 power off

cp -R -a $TIPI_DIR/setup/bin/* $TIPI_DISK/

