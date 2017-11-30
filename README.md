# TIPI

(Pronounced tip-ee)

Turn a Raspberry PI and some glue hardware into a TI Disk Drive and Network interface. 

Keep it open for further device extension.

# Level 2 IO (sector like) is not yet supported. You cannot use apps like DM2K to copy files yet.

What can we do:

DSR for file READ support:

* INTERNAL/DISPLAY, FIXED/VARIABLE, PROGRAM, DIRECTORY

Write support:

* INTERNAL/DISPLAY, FIXED/VARIABLE, PROGRAM

CATALOG support. 

* Sub-directory support.

Native file support:

* /b99 /bas /xb files can be LOADed or SAVEd as PROGRAM files with automatic transformation to/from ASCII native os files.
* /txt /a99 /b99 /bas /xb native os ascii files can be OPEN and READ as DISPLAY VARIABLE 80 files.
* other native os files can be OPEN and READ as DISPLAY FIXED 128 files.

Partial long name support

* CATALOG shows shortened names only
* Long names and short names supported for file access.

DSR devices: 

* TIPI. 
* DSK0. 
* DSK1. 
* DSK2. 
* DSK3. 
* DSK.

Special files:

* PI.CLOCK - reading a DISPLAY 24 record returns asctime (time & date as string)
* PI.STATUS - virtual D/V 80 file with list of network device info on PI. (mac addresses, and ip addresses for each network device )
* PI.HTTP://... - GETs an HTTP url and let you access it like a normal file.
* PI.TCP=hostname:port - open a socket, write opcode supported to write, read to read... 
* PI.STATUS - virtual D/V 80 file with version and network information.
* PI.CONFIG - virtual D/V 80 file for configuration of TIPI services.

File name transformation:

Devices are mapped to unix filesystem locations:

* TIPI. - /home/tipi/tipi_disk
* DSK0. - /home/tipi/tipi_disk ( alias for TIPI. for disk unit 0 support )
* DSK1. - /home/tipi/tipi_disk/DSK1
* DSK2. - /home/tipi/tipi_disk/DSK2
* DSK3. - /home/tipi/tipi_disk/DSK3
* DSK.<vol> - /home/tipi/tipi_disk/<vol>

DSK1-3 are managed as symlinks, and can be configured with the DMAP BASIC program.

Raspberry PI transforms TI device-filenames with the following rules:

* '.' in file or path names become '/'
* '/' or '\' in file or path names becomes '.'
* linux filenames with more than 10 characters can be referenced with either the long name, or the short hashed name
  as listed in the CATALOG
* there is no shortening support for directory names
* capitolization is observed ( the host os provides a case sensitive filesystem, as is the TI FS )

Examples:

```
+---------------------+-------------------------------------+
| TI NAME             | UNIX NAME                           |
+---------------------+-------------------------------------+
| TIPI.BAS.MYGAME     | /home/tipi/tipi_disk/BAS/MYGAME     |
| TIPI.BAS.MYGAME/B99 | /home/tipi/tipi_disk/BAS/MYGAME.B99 |
| TIPI.docs.race/md   | /home/tipi/tipi_disk/docs/race.md   |
| DSK.WB.FAVORITES    | /home/tipi/tipi_disk/WB/FAVORITES   |
+---------------------+-------------------------------------+
```

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

