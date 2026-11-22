#!/bin/bash

cd "$(dirname "$0")"
. ENV/bin/activate

export PATH=${TIPI_HOME:-/home/tipi}/xdt99:$PATH

export FLASK_APP=route.py

export FLASK_DEBUG=1

export TMPDIR=${TIPI_HOME:-/home/tipi}/web-tmp
mkdir -p $TMPDIR

python3 ./route.py
