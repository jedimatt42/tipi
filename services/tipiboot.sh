#!/bin/sh

# Things here run as root on system boot to make way for 
# standard boot services.

# /var/log is a tmpfs, need to add permissions on each boot
mkdir /var/log/tipi
chown tipi.tipi /var/log/tipi
ln -s /var/log/tipi /home/tipi/log

if [ ! -e /home/tipi/tipi.uuid ]; then
( echo "import uuid" ; echo "print uuid.uuid1()" ) | \
    python - >/home/tipi/tipi.uuid
fi

