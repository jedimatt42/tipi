#!/bin/bash

function deps() {
  sudo apt update
  sudo apt-get install -y imagemagick
  sudo apt-get install -y libpng12-dev
  sudo apt-get install -y libhpdf-2.3.0
  sudo apt-get install -y libhpdf-dev
  sudo apt-get install -y libsdl-dev
}

function build() {
  cd /home/tipi
  if [ ! -e PrinterToPDF ];
  then
    git clone https://github.com/jedimatt42/PrinterToPDF.git
  fi
  cd PrinterToPDF
  git pull
  gcc PrinterConvert.c `sdl-config --cflags --libs` -DPAPER_LETTER -o printerToPDF_Letter -lrt -lhpdf -lpng
  gcc PrinterConvert.c `sdl-config --cflags --libs` -o printerToPDF_A4 -lrt -lhpdf -lpng
}

function share() {
  mkdir -p /home/tipi/pdf_share
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
valid user=tipi
create mask=0644
directory mask=0755
force user=tipi

xxx
  cat /tmp/smb.a /tmp/smb.b | sudo tee /etc/samba/smb.conf
  sudo systemctl restart smbd
  rm -f /tmp/smb.a /tmp/smb.b
}

deps
build
grep "pdf_share" /etc/samba/smb.conf || share

