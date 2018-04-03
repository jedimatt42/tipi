#!/bin/bash

apt-get update
apt-get install -y libsqlite3-dev

su tipi -c "/home/tipi/tipi/services/update-deps.sh"
su tipi -c "/home/tipi/tipi/htdocs/update-deps.sh"
su tipi -c "cp /home/tipi/tipi/setup/bin/TIPI* /home/tipi/tipi_disk/"
su tipi -c "mkdir /home/tipi/tipi_disk/NET; cp /home/tipi/tipi/setup/bin/NET/* /home/tipi/tipi_disk/NET/"

# temporary... 
if [ -e /home/tipi/tipi/RUN/CHATTI ]; then
  su tipi -c "mkdir /home/tipi/.tipivars"
  su tipi -c "mv /home/tipi/tipi/RUN/* /home/tipi/.tipivars/"
  su tipi -c "rm -fr /home/tipi/tipi/RUN"
fi

cd /home/tipi/tipi/setup/

if [ -e /lib/systemd/system/tipioled.service ]; then
  systemctl stop tipioled.service
  systemctl disable tipioled.service
  rm /lib/systemd/system/tipioled.service
fi

systemctl stop tipi.service
systemctl stop tipiweb.service
systemctl stop tipimon.service
systemctl stop tipiwatchdog.service
systemctl stop tipiboot.service

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

# screw with .tipivars/CHATTI
if [ ! -f /home/tipi/.tipivars/GLOBAL ]; then
  cat /home/tipi/.tipivars/CHATTI | egrep "(REMOTE_HOST|SESSION_ID|PASSWORD|REMOTE_PORT)" >/home/tipi/.tipivars/GLOBAL
  mv /home/tipi/.tipivars/CHATTI /tmp/CHATTI
  cat /tmp/CHATTI | egrep -v "(REMOTE_HOST|SESSION_ID|PASSWORD|REMOTE_PORT)" >>/home/tipi/.tipivars/CHATTI
  sudo chown tipi.tipi /home/tipi/.tipivars/CHATTI
  sudo chown tipi.tipi /home/tipi/.tipivars/GLOBAL
fi

echo "upgrade complete"
