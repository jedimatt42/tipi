#!/bin/bash

cd /home/tipi/tipi/services

source ENV/bin/activate

cat /sys/firmware/devicetree/base/model | grep "Pi Zero W" >/dev/null 2>&1
if [ $? == 0 ]; then
  # signalling delay for PI Zero W
  export TIPI_SIG_DELAY=0
else
  # signalling delay for PI 3
  export TIPI_SIG_DELAY=50
fi

python ./TipiService.py

