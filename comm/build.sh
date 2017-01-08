#!/bin/bash

# Convert .bas text file to TI BASIC file
rm -fr build
mkdir -p build
xbas99.py -c comm_mm.bas -o build/COMM_MM

# Create a disk image with TI files on it
rm -f build/COMM.DSK
xdm99.py -X DSSD4T build/COMM.DSK
xdm99.py -a build/COMM_MM -n COMM_MM build/COMM.DSK 
xdm99.py -i build/COMM.DSK 


