# TIPI

(Pronounced tip-ee)

Turn a Raspberry PI and some glue hardware into a TI Disk Drive and Network interface. 

Keep it open for further device extension.

## Branching

(For end users starting from an SD card image, you are already on the correct branch)

- End users must be on one of the `_release` branches for physical TIPI
- `main` branch is full of stuff that doesn't work, won't upgrade correctly, and certainly won't downgrade
- `main` branch is expert mode only

Branches:

```
  main - current development for latest Raspberry PI OS
  bullseye_release - beta status 
  buster_dev - (legacy) for patching upstream of buster_release
  buster_release - (legacy) for Raspberry PI 2W - 4B+ or Qemu use.
```

## Documentation

Please refer to the [wiki](https://github.com/jedimatt42/tipi/wiki)

## License 

The hardware design files and TI-99 DSR ROM code are in the [hardware](hardware) folder and free for use under the [UNLICENSE.txt](hardware/UNLICENSE.txt) 

The remaining software contained in this repository are licensed under the terms of [GPLv3](https://www.gnu.org/licenses/quick-guide-gplv3.en.html)

These files are part of TiPi.

TiPi is free hardware design and software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

TiPi is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with TiPi SD Card Image.  If not, see [GNU Licenses](http://www.gnu.org/licenses/).

