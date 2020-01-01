#!/bin/bash

function deps() {
  sudo apt update
  sudo apt install imagemagick
  sudo apt install libpng12-dev
  sudo apt install libhpdf-2.3.0
  sudo apt install libhpdf-dev
  sudo apt install libsdl-dev
}

function build() {
  cd /home/tipi
  git clone https://github.com/RWAP/PrinterToPDF.git
  cd PrinterToPDF
  gcc PrinterConvert.c `sdl-config --cflags --libs` -o printerToPDF -lrt -lhpdf -lpng
}

function share() {
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

