#!/bin/bash

SCRIPT_DIR=$(dirname $0)
TIPI_DIR=$(cd $SCRIPT_DIR/..; pwd)
cd $TIPI_DIR/services

source ENV/bin/activate

source $TIPI_DIR/setup/tipi_paths.sh

export TIPI_SIG_DELAY=$(grep TIPI_SIG_DELAY $TIPI_CONF/tipi.config | cut -f2 -d=)

if [ -f /etc/rpi-issue ]; then
  if [ -z ${TIPI_SIG_DELAY:-} ]; then
    # default signalling delay for unknown device will be slow
    export TIPI_SIG_DELAY=200

    cat /proc/device-tree/model | grep "Pi Zero W Rev" >/dev/null 2>&1
    if [ $? = 0 ]; then
      # signalling delay for PI Zero W
      export TIPI_SIG_DELAY=0
    fi

    cat /proc/device-tree/model | grep "Pi 3 Model B Rev" >/dev/null 2>&1
    if [ $? = 0 ]; then
      # signalling delay for PI 3
      export TIPI_SIG_DELAY=100
    fi

    cat /proc/device-tree/model | grep "Pi 3 Model B Plus Rev" >/dev/null 2>&1
    if [ $? = 0 ]; then
      # signalling delay for PI 3+
      export TIPI_SIG_DELAY=100
    fi
  fi
fi

# run ../emulation/emu_setup.sh to configure for websocket server
echo "checking for operation mode..."
if [ -e $TIPI_CONF/.emulation ]; then
  echo "Enabling emulation web-socket"
  export TIPI_WEBSOCK=$TIPI_DIR/htdocs
  grep "PDF_ENABLED=0" $TIPI_CONF/.emulation >/dev/null
  if [ $? = 0 ]; then
    export TIPI_NO_PDF=true
  fi
else
  # the libtipi code will use 50 if not set at all, but that shouldn't be possible
  echo "TIPI_SIG_DELAY=${TIPI_SIG_DELAY:-50}"
fi

python ./TipiService.py

