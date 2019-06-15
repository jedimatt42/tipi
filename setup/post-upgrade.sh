#!/bin/bash

version=${1:-0}

# Version is the old version number. Variables should enable steps required to get to latest.

case $version in
0)
  TIPI_BASE_CONFIG=true
  TIPI_RESTART_SERVICES=true
  TIPI_UPDATE_DEPS=true
  ;;
*)
  TIPI_RESTART_SERVICES=true
  ;;
esac


#### Perform steps

if [ ! -z ${TIPI_RESTART_SERVICES:-} ]; then
systemctl stop tipi.service
systemctl stop tipiweb.service
systemctl stop tipimon.service
systemctl stop tipiwatchdog.service
systemctl stop tipiboot.service
fi

if [ ! -z ${TIPI_UPDATE_DEPS:-} ]; then
apt-get update
apt-get install -y libsqlite3-dev

su tipi -c "/home/tipi/tipi/services/update-deps.sh"
su tipi -c "/home/tipi/tipi/htdocs/update-deps.sh"
fi

#### Should have been part of base sd image creation
if [ ! -z ${TIPI_BASE_CONFIG:-} ]; then
usermod -s /bin/bash tipi
raspi-config nonint do_i2c 0
fi

#### Always update TI binaries (cheap)
su tipi -c "cp /home/tipi/tipi/setup/bin/TIPI* /home/tipi/tipi_disk/"
su tipi -c "mkdir -p /home/tipi/tipi_disk/NET; cp /home/tipi/tipi/setup/bin/NET/* /home/tipi/tipi_disk/NET/"

#### Restart all TIPI services
if [ ! -z ${TIPI_RESTART_SERVICES:-} ]; then
cd /home/tipi/tipi/setup/

cp *.service /lib/systemd/system/

systemctl enable tipiboot.service
systemctl enable tipiwatchdog.service
systemctl enable tipi.service
systemctl enable tipiweb.service
systemctl enable tipimon.service
systemctl enable tipisuper.service
# systemctl enable tipibutton.service

# the order below matters
systemctl restart tipiboot.service
systemctl restart tipiwatchdog.service
systemctl restart tipimon.service
systemctl restart tipiweb.service
# systemctl restart tipibutton.service
systemctl restart tipi.service

# last we'll restart the super service which is our parent process.
systemctl restart tipisuper.service
fi

echo "upgrade complete"
