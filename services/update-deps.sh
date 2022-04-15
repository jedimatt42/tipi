#!/bin/bash

SCRIPT_DIR=$(dirname $0)
TIPI_DIR=$(cd $SCRIPT_DIR/..; pwd)
cd $TIPI_DIR/services

source $TIPI_DIR/setup/tipi_paths.sh

./setup.sh

