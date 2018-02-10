#!/bin/bash

apt-get update
apt-get install -y libsqlite3-dev

su tipi -c "/home/tipi/tipi/services/update-deps.sh"
su tipi -c "/home/tipi/tipi/htdocs/update-deps.sh"
su tipi -c "cp /home/tipi/tipi/setup/bin/* /home/tipi/tipi_disk/"

# temporary... 
if [ -e /home/tipi/tipi/RUN/CHATTI ]; then
  su tipi -c "mkdir /home/tipi/.tipivars"
  su tipi -c "mv /home/tipi/tipi/RUN/* /home/tipi/.tipivars/"
  su tipi -c "rm -fr /home/tipi/tipi/RUN"
fi

cd /home/tipi/tipi/setup/

systemctl stop tipi.service
systemctl stop tipiweb.service
systemctl stop tipimon.service
systemctl stop tipioled.service
systemctl stop tipiwatchdog.service
systemctl stop tipiboot.service

cp *.service /lib/systemd/system/

systemctl enable tipiboot.service
systemctl enable tipiwatchdog.service
systemctl enable tipi.service
systemctl enable tipioled.service
systemctl enable tipiweb.service
systemctl enable tipimon.service
systemctl enable tipisuper.service

# the order below matters
systemctl restart tipiboot.service
systemctl restart tipiwatchdog.service
systemctl restart tipioled.service
systemctl restart tipimon.service
systemctl restart tipiweb.service
systemctl restart tipi.service

# last we'll restart the super service which is our parent process.
systemctl restart tipisuper.service

echo "upgrade complete"
