#!/bin/bash

TIPI=/home/tipi/tipi
cd $TIPI || exit 1

sudo apt-get -y install \
 python-dev \
 python3-dev \
 python3-pip \
 libcurl4-openssl-dev \
 libssl-dev \
 samba \
 sqlite3 \
 libsqlite3-dev \
 php \
 virtualenv

sudo apt-get -y install usbmount

if [ ! -e /home/tipi/tipi_disk ]; then
  mkdir /home/tipi/tipi_disk
fi

if [ -d /home/tipi/xdt99 ]; then
  rm -rf /home/tipi/xdt99
fi
( cd /home/tipi && git clone https://github.com/endlos99/xdt99.git )

if [ -d /home/tipi/tidbit ]; then
  rm -rf /home/tipi/tidbit
fi
( cd /home/tipi && git clone https://github.com/dnotq/tidbit.git )

( cd $TIPI/services && $TIPI/services/setup.sh )
( cd $TIPI/htdocs && $TIPI/htdocs/setup.sh )
( cd $TIPI/setup && $TIPI/setup/setup.sh )

