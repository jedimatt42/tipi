#!/bin/bash

cd /home/tipi/tipi/services

source ENV/bin/activate

# default signalling delay for unknown device will be slow
export TIPI_SIG_DELAY=200

cat /proc/device-tree/model | grep "Pi Zero W Rev" >/dev/null 2>&1
if [ $? == 0 ]; then
  # signalling delay for PI Zero W
  export TIPI_SIG_DELAY=0
fi

cat /proc/device-tree/model | grep "Pi 3 Model B Rev" >/dev/null 2>&1
if [ $? == 0 ]; then
  # signalling delay for PI 3
  export TIPI_SIG_DELAY=100
fi

cat /proc/device-tree/model | grep "Pi 3 Model B Plus Rev" >/dev/null 2>&1
if [ $? == 0 ]; then
  # signalling delay for PI 3+
  export TIPI_SIG_DELAY=100
fi

# Uncomment this line to enable websocket server
#export TIPI_WEBSOCK=/home/tipi/tipi/htdocs

python ./TipiService.py

