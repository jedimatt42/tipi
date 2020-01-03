#!/bin/bash

source=$1

function topdf() {
  fname=`basename --suffix=.prn $source`
  cd /home/tipi/PrinterToPDF
  mv $source ./Test1.prn

  PRINT=./printerToPDF_Letter
  PAPER=`echo $source | grep _a4`
  if [ ! -z ${PAPER:-} ]; then
    PRINT=./printerToPDF_A4
  fi

  ${PRINT} 3 0 font2/SIEMENS.C16 1 sdloff /home/tipi/pdfs

  mkdir -p /home/tipi/pdf_share

  echo "Merging pages into one PDF: "
  ls -1 /home/tipi/pdfs/pdf/*.pdf

  gs -o "/home/tipi/pdf_share/${fname}.pdf" -q -sDEVICE=pdfwrite -dPDFSETTINGS=/prepress `ls -1 /home/tipi/pdfs/pdf/*.pdf`

  rm -f /home/tipi/pdfs/pdf/* /home/tipi/pdfs/eps/*
  rm -f /tmp/print_*.prn
}

topdf 2>&1 >>/var/log/tipi/pio.log

