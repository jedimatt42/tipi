#!/bin/bash

function deps() {
  apt update
  apt-get install -y imagemagick
  apt-get install -y libpng12-dev
  apt-get install -y libhpdf-2.3.0
  apt-get install -y libhpdf-dev
  apt-get install -y libsdl-dev
}

function share() {
  su tipi -c "mkdir -p /home/tipi/pdf_share"
  cp /etc/samba/smb.conf /tmp/smb.a 
  cat >/tmp/smb.b <<xxx

[PDFS]
comment=TI-99/4A Print to PDF
path=/home/tipi/pdf_share
public=no
browseable=Yes
writeable=Yes
only guest=no
guest ok=Yes
create mask=0644
directory mask=0755
force user=tipi

xxx
  cat /tmp/smb.a /tmp/smb.b | tee /etc/samba/smb.conf
  systemctl restart smbd
  rm -f /tmp/smb.a /tmp/smb.b
}

deps
su tipi -c "/home/tipi/tipi/setup/compile_printToPDF.sh"
grep "pdf_share" /etc/samba/smb.conf || share

