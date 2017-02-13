
#
# : DSR for TIPI, multi purpose Raspberry PI enabled device. 
# 
# Use xas99 
#

all: tipi.hex

clean:
	rm *.list
	rm tipi.bin
	rm tipi.hex

tipi.bin: rom.a99 header.a99 vdp-io.a99 tipi-io.a99 powerup.a99 devices.a99
	xas99.py -R -b -L tipi.list -o $@ rom.a99
	mv $@_4000 $@

tipi.hex: tipi.bin bin2hex.py
	./bin2hex.py >$@

