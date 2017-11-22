#!/bin/bash

cd /home/tipi/tipi/setup/

systemctl stop tipiwatchdog.service
systemctl stop tipi.service
systemctl stop tipioled.service
systemctl stop tipiweb.service

cp *.service /lib/systemd/system/

systemctl enable tipiboot.service
systemctl enable tipiwatchdog.service
systemctl enable tipi.service
systemctl enable tipioled.service
systemctl enable tipiweb.service
systemctl enable tipisuper.service

systemctl restart tipiboot.service
systemctl restart tipiwatchdog.service
systemctl restart tipi.service
systemctl restart tipioled.service
systemctl restart tipiweb.service
systemctl restart tipisuper.service

echo "upgrade complete"
