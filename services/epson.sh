#!/bin/bash

SCRIPT_DIR=$(dirname $0)
TIPI_DIR=$(cd $SCRIPT_DIR/..; pwd)
cd $TIPI_DIR/services

source $TIPI_DIR/setup/tipi_paths.sh

source=$1

function topdf() {
  fname=`basename --suffix=.prn $source`
  cd $TIPI_CONF/PrinterToPDF
  mv $source ./Test1.prn

  PAPER=`echo $source | grep _a4`

  mkdir -p $TIPI_CONF/pdf_share
  mkdir -p $TIPI_CONF/pdfs

  echo "Converting spool ${source} to PDF pages"
  if [ ! -z ${PAPER:-} ]; then
    ./printerToPDF -o $TIPI_CONF/pdfs -f font2/SIEMENS.C16 -p 0 -m 0 ./Test1.prn
  else
    ./printerToPDF -o $TIPI_CONF/pdfs -f font2/SIEMENS.C16 -p 216,280 -m 6,0,1,0 ./Test1.prn
  fi

  echo "Merging pages into single PDF: "
  ls -1v $TIPI_CONF/pdfs/pdf/*.pdf

  gs -o "${TIPI_CONF}/pdf_share/${fname}.pdf" -q -sDEVICE=pdfwrite -dPDFSETTINGS=/prepress `ls -1v $TIPI_CONF/pdfs/pdf/*.pdf`

  rm -f $TIPI_CONF/pdfs/pdf/* $TIPI_CONF/pdfs/eps/*
  rm -f /tmp/print_*.prn
  echo "Job Complete!"
}

topdf 2>&1 >>$TIPI_CONF/tipi/pio.log

