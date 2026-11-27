#!/bin/bash

cd "$(dirname "$0")"

TIPI_HOME=${TIPI_HOME:-/home/tipi}

source ENV/bin/activate

export TIPI_SIG_DELAY=$(grep TIPI_SIG_DELAY $TIPI_HOME/tipi.config 2>/dev/null | cut -f2 -d=)

if [ -z ${TIPI_SIG_DELAY:-} ]; then
  # default signalling delay for unknown device will be slow
  export TIPI_SIG_DELAY=200

  cat /proc/device-tree/model 2>/dev/null | grep "Pi Zero W Rev" >/dev/null 2>&1
  if [ $? = 0 ]; then
    # signalling delay for PI Zero W
    export TIPI_SIG_DELAY=0
  fi

  cat /proc/device-tree/model 2>/dev/null | grep "Pi 3 Model B Rev" >/dev/null 2>&1
  if [ $? = 0 ]; then
    # signalling delay for PI 3
    export TIPI_SIG_DELAY=100
  fi

  cat /proc/device-tree/model 2>/dev/null | grep "Pi 3 Model B Plus Rev" >/dev/null 2>&1
  if [ $? = 0 ]; then
    # signalling delay for PI 3+
    export TIPI_SIG_DELAY=100
  fi

  cat /proc/device-tree/model 2>/dev/null | grep "Pi 5 Model B" >/dev/null 2>&1
  if [ $? = 0 ]; then
    # signalling delay for PI 5
    export TIPI_SIG_DELAY=120
  fi
fi

# touch $TIPI_HOME/.emulation to enable websocket server
echo "checking for operation mode..."
if [ -e $TIPI_HOME/.emulation ]; then
  echo "Enabling emulation web-socket"
  export TIPI_WEBSOCK=$(dirname "$PWD")/htdocs
  grep "PDF_ENABLED=0" $TIPI_HOME/.emulation >/dev/null
  if [ $? = 0 ]; then
    export TIPI_NO_PDF=true
  fi
else
  # the libtipi code will use 50 if not set at all, but that shouldn't be possible
  echo "TIPI_SIG_DELAY=${TIPI_SIG_DELAY:-50}"
fi

python ./TipiService.py

