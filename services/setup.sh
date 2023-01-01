#!/bin/bash

if [ -d ENV ]; then
  rm -r ENV
fi

virtualenv --python=python3 --system-site-packages ENV

. ./ENV/bin/activate

# build the tipiports_chardev library, but only if on a Raspberry PI OS
if [ -e /etc/rpi-issue ]; then
  ( cd libtipi_chardev; python ./setup.py install )
else
  echo skipping tipiports_chardev
fi

# build the tipiports_websocket library
if [ ! -d libtipi_web/sha1 ]; then
  ( cd libtipi_web; git clone https://github.com/clibs/sha1.git )
fi
echo installing tipiports_websocket
( cd libtipi_web; python ./setup.py install )

pip install -r requirements.txt

