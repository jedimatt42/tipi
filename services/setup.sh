#!/bin/bash

if [ -d ENV ]; then
  rm -r ENV
fi

virtualenv --python=python3 --system-site-packages ENV

. ./ENV/bin/activate

pip install -r requirements.txt

# build the tipiports_websocket library
if [ ! -d libtipi_web/sha1 ]; then
  ( cd libtipi_web; git clone https://github.com/clibs/sha1.git )
fi
echo installing tipiports_websocket
( cd libtipi_web; python ./setup.py install )

# build the tipiports_gpio library, but only if on a Raspberry PI OS
if [ -e /etc/rpi-issue ]; then
  ( cd libtipi_gpio; python ./setup.py install )
else
  echo skipping tipiports_gpio
fi

