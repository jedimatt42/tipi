#!/bin/bash

image=$1
source_dir=$2
xdt99=${TIPI_HOME:-/home/tipi}/xdt99

tmp_name=/tmp/`basename $source_dir`
python3 $xdt99/xdm99.py $tmp_name -X 1440

for f in ${source_dir}/*; do
  if [ -f $f ]; then
    python3 $xdt99/xdm99.py $tmp_name -t -a $f
  fi
done
mv $tmp_name $image
