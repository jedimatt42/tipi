#!/bin/bash

source=$1

function topdf() {
  fname=`basename --suffix=.prn $source`
  cd /home/tipi/PrinterToPDF
  mv $source ./Test1.prn
  ./printerToPDF 3 0 font2/SIEMENS.C16 1 sdloff /home/tipi/pdfs

  mkdir -p /home/tipi/pdf_share

  gs -o "/home/tipi/pdf_share/${fname}.pdf" -q -sDEVICE=pdfwrite -dPDFSETTINGS=/prepress `ls -1 /home/tipi/pdfs/pdf/*.pdf`

  rm -f /home/tipi/pdfs/pdf/* /home/tipi/pdfs/eps/*
  rm -f /tmp/print_*.prn
}

topdf 2>&1 >>/var/log/tipi/pio.log

