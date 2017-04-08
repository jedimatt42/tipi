# DSR for TIPI

Right, now we have a very simple xdt99 based build system for creating a rom targetting >4000 that is comprised
of one or more .a99 source files. It produces tipi.bin, and the script bin2hex.py converts that to tipi.hex which
is a format that can be embedded/included in a verilog FPGA source file.

## Architecture

The code for the DSR is in two halves. TMS9900 assembly code (.a99 files) support the TI operating system by responding to
device PAB (Peripheral Access Block) requests. These are copied to the Raspberry PI through the hardware interface, and interpretted/handled by the python code. 

The Raspberry PI runs the 'fileserver.py' script as a systemd service. This script looks at the devicename, translates 
file names to matching local filesystem files, and supports OPEN, READ, CLOSE, and LOAD operations. SAVE, and WRITE are not implemented yet, as we work on stabilizing the hardware.

TipiPorts.py - low level interface to Raspberry PI GPIO pins. Also listens to RESET line, and triggers a restart. 
TipiMessages.py - next level up, send or receive a bytearray
ti_files.py - utilities for validating the format of the hosted files, decoding the file meta-data, and extracting records
ti_names.py - translates TI names to host filesystem names. We ignore names in the TIFILES meta-data.
SpecialFiles.py - handles generation of psuedo files for read access like TIPI.CLOCK and TIPI.STATUS.
fileserver.py - the primary service script, that loops waiting for DSR requests. Opcode handling and Catalog handling is in here too.


