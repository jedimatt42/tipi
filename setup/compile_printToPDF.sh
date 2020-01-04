#!/bin/bash

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

build

