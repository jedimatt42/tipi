#!/bin/bash

SCRIPT_DIR=$(dirname $0)
TIPI_DIR=$(cd $SCRIPT_DIR/..; pwd)
cd $TIPI_DIR/services

source ENV/bin/activate

source $TIPI_DIR/setup/tipi_paths.sh

python ./TipiSuper.py

