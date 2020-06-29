#!/bin/bash

if [ -d ENV ]; then
  rm -r ENV
fi

virtualenv --python=python3 --system-site-packages ENV

. ./ENV/bin/activate

if [ ! -d libtipi/sha1 ]; then
  ( cd libtipi; git clone https://github.com/clibs/sha1.git )
fi
( cd libtipi; python ./setup.py install )

pip install -r requirements.txt

