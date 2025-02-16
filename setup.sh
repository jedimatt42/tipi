#!/bin/bash

TIPI=/home/tipi/tipi
cd $TIPI || exit 1

set -o errexit

. /etc/os-release
if [ ${VERSION_CODENAME:-} = "bullseye" ]; then
  OSPKGS=python-dev
fi
if [ ${VERSION_CODENAME:-} = "bookworm" ]; then
  OSPKGS=python-dev-is-python3
fi

sudo apt-get remove --purge -y inetutils-telnetd inetutils-inetd inetutils-syslogd tcpd update-inetd

sudo apt-get -y install \
 $OSPKGS \
 python3-dev \
 python3-pip \
 libcurl4-openssl-dev \
 libssl-dev \
 samba \
 sqlite3 \
 libsqlite3-dev \
 php \
 virtualenv \
 telnetd-ssl

# sudo apt-get -y install usbmount

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

