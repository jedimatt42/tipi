#!/bin/bash

su tipi -c "/home/tipi/tipi/services/update-deps.sh"
su tipi -c "/home/tipi/tipi/htdocs/update-deps.sh"
su tipi -c "cp /home/tipi/tipi/setup/bin/* /home/tipi/tipi_disk/"

cd /home/tipi/tipi/setup/

systemctl stop tipiwatchdog.service
systemctl stop tipi.service
systemctl stop tipioled.service
systemctl disable tipioled.service
systemctl stop tipiweb.service
systemctl stop tipimon.service

cp *.service /lib/systemd/system/

systemctl enable tipiboot.service
systemctl enable tipiwatchdog.service
systemctl enable tipi.service
systemctl enable tipiweb.service
systemctl enable tipimon.service
systemctl enable tipisuper.service

systemctl restart tipiboot.service
systemctl restart tipiwatchdog.service
systemctl restart tipi.service
systemctl restart tipiweb.service
systemctl restart tipimon.service
systemctl restart tipisuper.service

echo "upgrade complete"
