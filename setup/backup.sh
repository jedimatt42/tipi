#!/bin/bash

id=`id -u`
if [ "x${id}" != "x0" ]; then
  echo "must run as root"
  exit 1
fi

TIMESTAMP=`date -Isecond | sed 's/://g'`

ARCHIVE=$TIPI_CONF/tipi-backup-${TIMESTAMP}.tar.gz 

WPATMP=$TIPI_CONF/tmp_wpa_supplicant.conf

FILE_LIST=/tmp/backup_list
if [ -d $TIPI_CONF/pdf_share ]; then
  echo pdf_share >$FILE_LIST
fi
if [ -d $TIPI_DISK ]; then
 echo tipi_disk >>$FILE_LIST
fi
if [ -d $TIPI_CONF/.tipivars ]; then
 echo .tipivars >>$FILE_LIST
fi
if [ -f $TIPI_CONF/tipi.config ]; then
 echo tipi.config >>$FILE_LIST
fi
if [ -f $TIPI_CONF/tipi.uuid ]; then
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
rm -f ${FILE_LIST}

