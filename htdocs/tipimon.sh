#!/bin/bash

cd /home/tipi/tipi/htdocs
. ENV/bin/activate

export PATH=/home/tipi/xdt99:$PATH

python ./tipi_monitor.py

