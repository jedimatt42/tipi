#!/bin/bash

UDEVD_SERVICE=/lib/systemd/system/systemd-udevd.service
TIPI_USB=/home/tipi/tipi_disk/USB

apt-get -y install usbmount

if [ -f $UDEVD_SERVICE ]; then
  sed -i s/PrivateMounts=yes/PrivateMounts=no/ /lib/systemd/system/systemd-udevd.service
fi

if [ ! -e $TIPI_USB ]; then
  ln -s /media/usb0 $TIPI_USB
  chown tipi.tipi $TIPI_USB
fi

