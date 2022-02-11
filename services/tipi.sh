#!/bin/bash

cd /home/tipi/tipi/services

source ENV/bin/activate

export TIPI_SIG_DELAY=$(grep TIPI_SIG_DELAY /home/tipi/tipi.config | cut -f2 -d=)

if [ -z ${TIPI_SIG_DELAY:-} ]; then
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
fi

# touch /home/tipi/.emulation to enable websocket server
echo "checking for operation mode..."
if [ -e /home/tipi/.emulation ]; then
  echo "Enabling emulation web-socket"
  export TIPI_WEBSOCK=/home/tipi/tipi/htdocs
else
  # the libtipi code will use 50 if not set at all, but that shouldn't be possible
  echo "TIPI_SIG_DELAY=${TIPI_SIG_DELAY:-50}"
fi

python ./TipiService.py

