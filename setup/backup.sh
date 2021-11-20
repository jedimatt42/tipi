#!/bin/bash

id=`id -u`
if [ "x${id}" != "x0" ]; then
  echo "must run as root"
  exit 1
fi

TIMESTAMP=`date -Isecond | sed 's/://g'`

ARCHIVE=/home/tipi/tipi-backup-${TIMESTAMP}.tar.gz 

WPATMP=/home/tipi/tmp_wpa_supplicant.conf

FILE_LIST=/tmp/backup_list
if [ -d /home/tipi/pdf_share ]; then
  echo pdf_share >$FILE_LIST
fi
if [ -d /home/tipi/tipi_disk ]; then
 echo tipi_disk >>$FILE_LIST
fi
if [ -d /home/tipi/.tipivars ]; then
 echo .tipivars >>$FILE_LIST
fi
if [ -f /home/tipi/tipi.config ]; then
 echo tipi.config >>$FILE_LIST
fi
if [ -f /home/tipi/tipi.uuid ]; then
 echo tipi.uuid >>$FILE_LIST
fi
if [ -f /etc/wpa_supplicant/wpa_supplicant.conf ]; then
 cp /etc/wpa_supplicant/wpa_supplicant.conf ${WPATMP}
 chown tipi.tipi ${WPATMP}
 echo tmp_wpa_supplicant.conf >>$FILE_LIST
fi

tar -cvzf ${ARCHIVE} \
  -C /home/tipi \
  --owner=tipi \
  --exclude=tipi_disk/TIPICF? \
  --exclude=tipi_disk/NET \
  --one-file-system \
  --files-from=${FILE_LIST}

chown tipi.tipi ${ARCHIVE}
rm -f ${WPATMP}

