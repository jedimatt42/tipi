#!/bin/bash

function build() {
  cd $TIPI_CONF
  if [ -d PrinterToPDF ];
  then
    rm -fr $TIPI_CONF/PrinterToPDF
  fi
  git clone https://github.com/RWAP/PrinterToPDF.git
  cd PrinterToPDF
  git pull
  make printerToPDF
}

build

