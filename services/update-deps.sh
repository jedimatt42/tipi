#!/bin/bash

if [ ! -d ENV ]; then
  virtualenv --system-site-packages ENV
fi

. ./ENV/bin/activate

( cd libtipi ; ./rebuild.sh )

pip install -r requirements.txt

