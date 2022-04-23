#!/bin/bash

cd /home/tipi
if [ ! -d /home/tipi/tipi_disk ]; then
  mkdir /home/tipi/tipi_disk
fi

if [ ! -d /home/tipi/xdt99 ]; then
  git clone https://github.com/endlos99/xdt99.git
fi

if [ ! -d /home/tipi/tidbit ]; then
  git clone https://github.com/dontq/tidbit.git
fi

if [ ! -d /home/tipi/tipi ]; then
  git clone https://github.com/jedimatt42/tipi.git 
  cd tipi
  git checkout jm42/docker
  git submodule update --init
  cd services
  ./setup.sh
  ( cd ../htdocs; ./setup.sh )
fi

if [ ! -f /home/tipi/.emulation ]; then
  echo "# TIPI WEBSOCKET" >/home/tipi/.emulation
  echo "NFS_ENABLED=0" >>/home/tipi/.emulation
  echo "PDF_ENABLED=1" >>/home/tipi/.emulation
fi

cd /home/tipi/tipi/services
exec ./tipi-emu.sh
