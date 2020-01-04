#!/bin/bash

function build() {
  cd /home/tipi
  if [ ! -e PrinterToPDF ];
  then
    git clone https://github.com/jedimatt42/PrinterToPDF.git
  fi
  cd PrinterToPDF
  git pull
  gcc PrinterConvert.c `sdl-config --cflags --libs` -o printerToPDF -lrt -lhpdf -lpng
}

build

