# Memory Map

All TI peripherals are allowed to page into the 4A memory map between 0x4000 and 0x5FFF. In order to minimize the interference of a paged in DSR rom the IO memory ports are the last 4 words (8 bytes) in the DSR rom space. 

Address assignments:

* 5FFF - ( 0101 1111 1111 1111 ) - 8 bit TI -> RPi Data
* 5FFE - undefined
* 5FFD - ( 0101 1111 1111 1101 ) - 8 bit TI -> RPi Control Signals
* 5FFC - undefined
* 5FFB - ( 0101 1111 1111 1011 ) - 8 bit RPi -> TI Data
* 5FFA - undefined
* 5FF9 - ( 0101 1111 1111 1001 ) - 4 bit RPi -> TI Control Signals
* 5FF8 - undefined

Remember the TI-99/4A performs memory IO in 16 bits. We will use least significant bytes only, to avoid any software issues with the TMS9900 read before write behavior.  Further, signalling bits are at separate words from data to mandate that data is always ready a cycle before signaling indicates it is ready.


