#!/bin/bash

systemctl stop tipi.service
systemctl stop tipiweb.service
systemctl stop tipimon.service
systemctl stop tipiwatchdog.service
systemctl stop tipiboot.service

apt-get update
apt-get install -y libsqlite3-dev

raspi-config nonint do_i2c 0

su tipi -c "/home/tipi/tipi/services/update-deps.sh"
su tipi -c "/home/tipi/tipi/htdocs/update-deps.sh"
su tipi -c "cp /home/tipi/tipi/setup/bin/TIPI* /home/tipi/tipi_disk/"
su tipi -c "mkdir /home/tipi/tipi_disk/NET; cp /home/tipi/tipi/setup/bin/NET/* /home/tipi/tipi_disk/NET/"

usermod -s /bin/bash tipi

cd /home/tipi/tipi/setup/

cp *.service /lib/systemd/system/

systemctl enable tipiboot.service
systemctl enable tipiwatchdog.service
systemctl enable tipi.service
systemctl enable tipiweb.service
systemctl enable tipimon.service
systemctl enable tipisuper.service

# the order below matters
systemctl restart tipiboot.service
systemctl restart tipiwatchdog.service
systemctl restart tipimon.service
systemctl restart tipiweb.service
systemctl restart tipi.service

# last we'll restart the super service which is our parent process.
systemctl restart tipisuper.service

echo "upgrade complete"
