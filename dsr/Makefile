
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

tipi.bin: header.a99
	xas99.py -R -b -L tipi.list -o $@ $<
	mv $@_4000 $@

tipi.hex: tipi.bin
	./bin2hex.py >$@

