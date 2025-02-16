#!/bin/bash

set -o errexit

echo "Installing PI.PIO support..."
cd /home/tipi/tipi/setup/
sudo ./printing_setup.sh

echo "Configuring OS services..."
cd /home/tipi/tipi/setup/etc
sudo cp ./hosts.allow /etc/hosts.allow
sudo cp ./hosts.deny /etc/hosts.deny
sudo cp ./samba/smb.conf /etc/samba/smb.conf

echo "Installing systemd services..."

cd /home/tipi/tipi/setup/
sudo cp *.service /lib/systemd/system/
sudo systemctl enable tipiboot.service
sudo systemctl restart tipiboot.service
sudo systemctl enable tipiwatchdog.service
sudo systemctl restart tipiwatchdog.service
sudo systemctl enable tipi.service
sudo systemctl restart tipi.service
sudo systemctl enable tipisuper.service
sudo systemctl restart tipisuper.service
sudo systemctl enable tipimon.service
sudo systemctl restart tipimon.service
sudo systemctl enable tipiweb.service
sudo systemctl restart tipiweb.service

sudo systemctl status tipi.service
sudo systemctl status tipiweb.service

