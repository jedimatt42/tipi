#!/bin/bash

TIPI=/home/tipi/tipi
cd $TIPI || exit 1

sudo apt-get install python-dev
sudo apt-get install python-virtualenv
sudo apt-get install python-imaging
sudo apt-get install libcurl4-openssl-dev
sudo apt-get install libssl-dev
sudo apt-get install libjpeg-dev
sudo apt-get install wiringpi
sudo apt-get install samba
sudo apt-get install sqlite3
sudo apt-get install libsqlite3-dev

if [ ! -e /home/tipi/tipi_disk ]; then
  mkdir /home/tipi/tipi_disk
fi

if [ -d /home/tipi/xdt99 ]; then
  rm -r /home/tipi/xdt99
fi
( cd /home/tipi && git clone https://github.com/endlos99/xdt99.git )

( cd $TIPI/services && $TIPI/services/setup.sh )
( cd $TIPI/htdocs && $TIPI/htdocs/setup.sh )
( cd $TIPI/setup && $TIPI/setup/setup.sh )

