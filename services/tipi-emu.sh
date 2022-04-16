#!/bin/bash

cd /home/tipi/tipi/services

source ENV/bin/activate

# touch /home/tipi/.emulation to enable websocket server
echo "Enabling emulation web-socket"
export TIPI_WEBSOCK=/home/tipi/tipi/htdocs
grep "PDF_ENABLED=0" /home/tipi/.emulation >/dev/null
if [ $? = 0 ]; then
  export TIPI_NO_PDF=true
fi

if [ ! -e /home/tipi/tipi.uuid ]; then
  ( echo "import uuid" ; echo "print(uuid.uuid1())" ) | \
    python3 - >/home/tipi/tipi.uuid
fi

cp -R -a /home/tipi/tipi/setup/bin/* /home/tipi/tipi_disk/

export TIPI_NO_LOG=true

while true; do
  python ./TipiService.py
  sleep 1
done

