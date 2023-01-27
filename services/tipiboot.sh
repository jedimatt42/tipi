#!/bin/sh

# Things here run as root on system boot to make way for 
# standard boot services.

# Check /boot for a backup file
BACKUP=`ls -1 /boot/tipi-backup-*.tar.gz 2>/dev/null`
if [ -f ${BACKUP:-notfile} ]; then
  /home/tipi/tipi/setup/restore.sh $BACKUP
fi

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
  grep "NFS_ENABLED=1" /home/tipi/.emulation >/dev/null
  if [ $? = 0 ]; then
    # mount nfs from host OS
    HOSTIP=`ip route | grep default | cut -d' ' -f3`
    mount -t nfs ${HOSTIP}:/tipi_disk /home/tipi/tipi_disk
  fi
else
  # not emulation, so make sure the kernel module is loaded
  if [ -f /home/tipi/tipi_kernel_module/onboot.sh ]; then
    /home/tipi/tipi_kernel_module/onboot.sh
  fi
  chmod a+rw /dev/tipi_control
  chmod a+rw /dev/tipi_data
fi

# disable power management for the wifi
iwconfig wlan0 power off

cp -R -a /home/tipi/tipi/setup/bin/* /home/tipi/tipi_disk/

