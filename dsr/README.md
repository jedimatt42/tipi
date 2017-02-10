# DSR for TIPI

Right, now we have a very simple xdt99 based build system for creating a rom targetting >4000 that is comprised
of one or more .a99 source files. It produces tipi.bin, and the script bin2hex.py converts that to tipi.hex which
is a format that can be embedded/included in a verilog FPGA source file.

