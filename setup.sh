#!/bin/bash

TIPI=/home/tipi/tipi
cd $TIPI || exit 1

sudo adduser tipi gpio
sudo adduser tipi input
sudo adduser tipi i2c

if [ -d /home/tipi/xdt99 ]; then
  rm -r /home/tipi/xdt99
fi
( cd /home/tipi && git clone https://github.com/endlos99/xdt99.git )

( cd $TIPI/services && $TIPI/services/setup.sh )
( cd $TIPI/htdocs && $TIPI/htdocs/setup.sh )
( cd $TIPI/setup && $TIPI/setup/setup.sh )

