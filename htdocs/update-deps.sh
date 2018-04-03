#!/bin/bash

cd /home/tipi/tipi/htdocs

if [ ! -d ENV ]; then
  virtualenv --system-site-packages ENV
fi

. ./ENV/bin/activate

pip install -r requirements.txt

