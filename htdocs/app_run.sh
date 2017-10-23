#!/bin/bash

cd /home/tipi/htdocs
. ENV/bin/activate

export PATH=/home/tipi/xdt99:$PATH

export FLASK_APP=route.py

export FLASK_DEBUG=1

flask run --host=0.0.0.0 --port 9900
