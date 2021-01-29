#!/bin/bash

source=$1

function topdf() {
  fname=`basename --suffix=.prn $source`
  cd /home/tipi/PrinterToPDF
  mv $source ./Test1.prn

  PAPER=`echo $source | grep _a4`

  echo "Converting spool ${source} to PDF pages"
  if [ ! -z ${PAPER:-} ]; then
    ./printerToPDF -8 -o /home/tipi/pdfs -f font2/SIEMENS.C16 -p 0 -m 0 ./Test1.prn
  else
    ./printerToPDF -8 -o /home/tipi/pdfs -f font2/SIEMENS.C16 -p 2 -m 0 ./Test1.prn
  fi

  mkdir -p /home/tipi/pdf_share

  echo "Merging pages into single PDF: "
  ls -1v /home/tipi/pdfs/pdf/*.pdf

  gs -o "/home/tipi/pdf_share/${fname}.pdf" -q -sDEVICE=pdfwrite -dPDFSETTINGS=/prepress `ls -1v /home/tipi/pdfs/pdf/*.pdf`

  rm -f /home/tipi/pdfs/pdf/* /home/tipi/pdfs/eps/*
  rm -f /tmp/print_*.prn
  echo "Job Complete!"
}

topdf 2>&1 >>/var/log/tipi/pio.log

