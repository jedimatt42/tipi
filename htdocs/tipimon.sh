#!/bin/bash

cd "$(dirname "$0")"
. ENV/bin/activate

export PATH=${TIPI_HOME:-/home/tipi}/xdt99:$PATH

python ./tipi_monitor.py

