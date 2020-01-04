#!/bin/bash

source=$1

# pageWidth,pageLength,leftMargin,rightMargin,topMargin,bottomMargin
PAPER_A4=5954,8417,85,85,85,85
PAPER_LETTER=6120,7920,85,85,22,22

function topdf() {
  fname=`basename --suffix=.prn $source`
  cd /home/tipi/PrinterToPDF
  mv $source ./Test1.prn

  PAPER=`echo $source | grep _a4`
  if [ ! -z ${PAPER:-} ]; then
    export PAPER_DIMS=$PAPER_A4
  else
    export PAPER_DIMS=$PAPER_LETTER
  fi

  echo "Converting spool ${source} to PDF pages"
  ./printerToPDF 3 0 font2/SIEMENS.C16 1 sdloff /home/tipi/pdfs

  mkdir -p /home/tipi/pdf_share

  echo "Merging pages into single PDF: "
  ls -1v /home/tipi/pdfs/pdf/*.pdf

  gs -o "/home/tipi/pdf_share/${fname}.pdf" -q -sDEVICE=pdfwrite -dPDFSETTINGS=/prepress `ls -1v /home/tipi/pdfs/pdf/*.pdf`

  rm -f /home/tipi/pdfs/pdf/* /home/tipi/pdfs/eps/*
  rm -f /tmp/print_*.prn
  echo "Job Complete!"
}

topdf 2>&1 >>/var/log/tipi/pio.log

