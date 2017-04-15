#!/bin/bash

# Convert .bas text file to TI BASIC file
rm -fr build
mkdir -p build
mkdir -p build/tifiles
xbas99.py -c test1.bas -o build/TEST1

# copy TIFILES format file to /tipi_disk/TEST1
xdm99.py -T build/TEST1 -o build/tifiles/TEST1

# catalog/directory listing program
xbas99.py -c catalog.bas -o build/CAT
xdm99.py -T build/CAT -o build/tifiles/CAT

# ascii clock display
xbas99.py -c clock.bas -o build/CLOCK
xdm99.py -T build/CLOCK -o build/tifiles/CLOCK

# HTTP Request
xbas99.py -c get.bas -o build/GET
xdm99.py -T build/GET -o build/tifiles/GET

