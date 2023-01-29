#!/bin/bash

function build() {
  cd /home/tipi
  if [ -d PrinterToPDF ];
  then
    rm -fr /home/tipi/PrinterToPDF
  fi
  # git clone https://github.com/RWAP/PrinterToPDF.git
  git clone https://github.com/jedimatt42/PrinterToPDF.git
  cd PrinterToPDF
  git checkout jm42/aarch64_support
  git pull
  make printerToPDF
}

build

