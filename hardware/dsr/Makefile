
#
# : DSR for TIPI, multi purpose Raspberry PI enabled device. 
# 
# Use xas99 
#

all: tipi.bin

sources = rom.a99 header.a99 vdp-io.a99 tipi-io.a99 powerup.a99 devices.a99 loadea5.a99 opt5.a99 basic.a99 level2.a99 dsrlist.a99

clean:
	-rm *.list >/dev/null 2>&1
	-rm tipi*.bin >/dev/null 2>&1

tipi0.bin: $(sources)
	xas99.py -R -b -L tipi0.list -o $@ rom.a99 -DA14=0
	mv $@_4000 $@
	dd if=/dev/null of=$@ bs=1 count=0 seek=16384

tipi1.bin: $(sources)
	xas99.py -R -b -L tipi1.list -o $@ rom.a99 -DA14=1
	mv $@_4000 $@
	dd if=/dev/null of=$@ bs=1 count=0 seek=16384

tipi.bin: tipi0.bin tipi1.bin
	cat tipi0.bin tipi1.bin >$@

.PHONY: burn

burn: tipi.bin
	minipro -p "AM27C256 @DIP28" -w tipi.bin -y

