# pi-messaging

Exploring a generalized mechanism for 8 bit messaging between a TI-99/4A and
a Raspberry PI 3

What can we do:

DSR for file READ support:
  INTERNAL/DISPLAY, FIXED/VARIABLE, PROGRAM, DIRECTORY

CATALOG support. 
Sub-directory support.

Partial long name support

* CATALOG shows shortened names only
* Long names and short names supported for file access.

DSR devices: 

* TIPI. 
* DSK1. 
* DSK.

Special files:

* TIPI.CLOCK - reading a DISPLAY 24 record returns asctime (time & date as string)
* TIPI.STATUS - virtual D/V 80 file with list of network device info on PI. (mac addresses, and ip addresses for each network device )
* TIPI.HTTP://... - GETs an HTTP url and let you access it like a normal file.
* TIPI.TCP=hostname:port - open a socket, write opcode supported to write, read to read... 

Low level support:

* USB Mouse support - client library for GCC.
* More to come ( TCP, UDP, NETWORK-VARIABLES )

## Who: 

* ElectricLab
* Jedimatt42

## Documentation

Please refer to the wiki.

## License 

The designs files and software contained in this repository are licenses under the terms of [GPLv3](https://www.gnu.org/licenses/quick-guide-gplv3.en.html)

These files are part of TiPi.

TiPi is free hardware design and software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

TiPi is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with TiPi.  If not, see [GNU Licenses](http://www.gnu.org/licenses/).

