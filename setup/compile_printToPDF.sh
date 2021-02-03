#!/bin/bash

function build() {
  cd /home/tipi
  if [ -d PrinterToPDF ];
  then
    rm -fr /home/tipi/PrinterToPDF
  fi
  git clone https://github.com/RWAP/PrinterToPDF.git
  cd PrinterToPDF
  git pull
  make printerToPDF
}

build

