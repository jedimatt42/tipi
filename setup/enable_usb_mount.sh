#!/bin/bash

UDEVD_SERVICE=/lib/systemd/system/systemd-udevd.service
TIPI_USB=/home/tipi/tipi_disk/USB

apt-get -y install usbmount

if [ -f $UDEVD_SERVICE ]; then
  sed -i s/PrivateMounts=yes/PrivateMounts=no/ /lib/systemd/system/systemd-udevd.service
fi

if [ -e $TIPI_USB ]; then
  rm $TIPI_USB
fi

cp /home/tipi/tipi/setup/01_expose_to_tipi /etc/usbmount/mount.d/
cp /home/tipi/tipi/setup/01_remove_from_tipi /etc/usbmount/umount.d/

