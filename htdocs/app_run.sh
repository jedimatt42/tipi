#!/bin/bash

cd /home/tipi/tipi/htdocs
. ENV/bin/activate

export PATH=/home/tipi/xdt99:$PATH

export FLASK_APP=route.py

export FLASK_DEBUG=1

python ./route.py
