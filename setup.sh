#!/bin/bash

TIPI=/home/tipi/tipi
cd $TIPI || exit 1

sudo apt-get install \
 python-dev \
 python3-dev \
 python-virtualenv \
 libcurl4-openssl-dev \
 libssl-dev \
 wiringpi \
 samba \
 sqlite3 \
 libsqlite3-dev \
 php

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

