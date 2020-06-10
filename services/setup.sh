#!/bin/bash

if [ -d ENV ]; then
  rm -r ENV
fi

virtualenv --python=python3 --system-site-packages ENV

. ./ENV/bin/activate

( cd libtipi; python ./setup.py install )

pip install -r requirements.txt

