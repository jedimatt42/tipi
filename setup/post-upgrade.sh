#!/bin/bash

fversion=${1:-0}
fmajor=`echo $fversion | cut -f1 -d.`
fminor=`echo $fversion | cut -f2 -d.`
nversion=`cat /home/tipi/tipi/version.txt | sed -n 's/^version=\(.*\)$/\1/p'`
nmajor=`echo $nversion | cut -f1 -d.`
nminor=`echo $nversion | cut -f2 -d.`

# $fversion is the old version number. $fmajor and $fminor are component integers
# $nversion is the new version number. $nmajor and $nminor are component integers
# Variables should enable steps required to get to latest.

if [ -e /home/tipi/.js99er ]; then
  mv /home/tipi/.js99er /home/tipi/.emulation
fi

case $fversion in
0)
  TIPI_BASE_CONFIG=true
  TIPI_RESTART_SERVICES=true
  TIPI_UPDATE_DEPS=true
  ;;
*)
  TIPI_RESTART_SERVICES=true
  ;;
esac

if [ -e /tmp/test_update ]; then
  TIPI_UPDATE_LIBTIPI=true
fi

if [ $fmajor -le 2 ] && [ $fminor -le 5 ]; then
  TIPI_UPDATE_LIBTIPI=true
fi

if [ $fmajor -le 2 ] && [ $fminor -le 4 ]; then
  TIPI_UPDATE_DEPS=true
fi

if [ $fmajor -le 1 ] && [ $fminor -le 47 ]; then
  TIPI_PURGE_CACHE=true
fi

if [ ! -d "/home/tipi/PrinterToPDF" ]; then
  TIPI_PRINTING_UPDATE=true
fi

#### Perform steps

su tipi -c "cd /home/tipi/tipi && git submodule update --init"

if [ ! -z ${TIPI_RESTART_SERVICES:-} ]; then
  systemctl stop tipi.service
  systemctl stop tipiweb.service
  systemctl stop tipimon.service
  systemctl stop tipiwatchdog.service
  systemctl stop tipiboot.service
fi

if [ ! -z ${TIPI_UPDATE_DEPS:-} ]; then
  apt-get update
  apt-get upgrade -y
  apt-get install -y libsqlite3-dev
  apt-get install -y python-pil
  apt-get install -y python3-dev
  # moves to the python3 version of xdt99
  su tipi -c "cd /home/tipi/xdt99/; git pull"

  su tipi -c "/home/tipi/tipi/services/update-deps.sh"
  su tipi -c "/home/tipi/tipi/htdocs/update-deps.sh"
fi

if [ ! -z ${TIPI_UPDATE_LIBTIPI:-} ]; then
  su tipi -c "/home/tipi/tipi/services/libtipi/rebuild.sh"
fi

if [ ! -f "/usr/bin/php" ]; then
  apt-get install -y php
fi

if [ ! -f "/home/tipi/tidbit/tidbit_cmd.php" ]; then
  su tipi -c "git clone https://github.com/dnotq/tidbit.git /home/tipi/tidbit"
fi

#### Should have been part of base sd image creation
if [ ! -z ${TIPI_BASE_CONFIG:-} ]; then
  usermod -s /bin/bash tipi
  if [ ! -e /home/tipi/.emulation ]; then
    raspi-config nonint do_i2c 0
  fi
fi

#### Always update TI binaries (cheap)
su tipi -c "cp /home/tipi/tipi/setup/bin/TIPI* /home/tipi/tipi_disk/"
su tipi -c "mkdir -p /home/tipi/tipi_disk/NET; cp /home/tipi/tipi/setup/bin/NET/* /home/tipi/tipi_disk/NET/"

#### Rebuild the printing to PDF converter and add samba share
if [ ! -z ${TIPI_PRINTING_UPDATE:-} ]; then
  /home/tipi/tipi/setup/printing_setup.sh
fi

#### Purge tipi_cache sqlite database if necessary
if [ ! -z ${TIPI_PURGE_CACHE:-} ]; then
  rm -f /home/tipi/.tipiweb.db
fi

#### Update tipi user group membership
sudo usermod -G tipi,sudo,input,i2c,gpio,adm tipi

#### Restart all TIPI services
if [ ! -z ${TIPI_RESTART_SERVICES:-} ]; then
  cd /home/tipi/tipi/setup/

  cp *.service /lib/systemd/system/

  systemctl enable tipiboot.service
  systemctl enable tipi.service
  systemctl enable tipiweb.service
  systemctl enable tipimon.service
  systemctl enable tipisuper.service
  # systemctl enable tipibutton.service

  # the order below matters
  systemctl restart tipiboot.service
  systemctl restart tipimon.service
  systemctl restart tipiweb.service
  # systemctl restart tipibutton.service
  systemctl restart tipi.service

  if [ ! -e /home/tipi/.emulation ]; then
    systemctl enable tipiwatchdog.service
    systemctl restart tipiwatchdog.service
  fi

  # last we'll restart the super service which is our parent process.
  systemctl restart tipisuper.service
fi

echo "upgrade complete"
