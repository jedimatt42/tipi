#!/bin/bash

echo "Installing systemd services..."

cd /home/tipi/tipi/services/systemd
sudo cp *.service /lib/systemd/system/
sudo systemctl enable tipiboot.service
sudo systemctl restart tipiboot.service
sudo systemctl enable tipiwatchdog.service
sudo systemctl restart tipiwatchdog.service
sudo systemctl enable tipi.service
sudo systemctl restart tipi.service
sudo systemctl enable tipioled.service
sudo systemctl restart tipioled.service
sudo systemctl enable tipisuper.service
sudo systemctl restart tipisuper.service
sudo systemctl enable tipiweb.service
sudo systemctl restart tipiweb.service

sudo systemctl status tipi.service
sudo systemctl status tipiweb.service

