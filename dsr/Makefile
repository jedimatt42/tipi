
#
# : DSR for TIPI, multi purpose Raspberry PI enabled device. 
# 
# Use xas99 
#

all: tipi.hex tipi_emu.bin reversed.bin

sources = rom.a99 header.a99 vdp-io.a99 tipi-io.a99 powerup.a99 devices.a99 basic.a99 level2.a99 blwpvec.a99

clean:
	rm *.list
	rm tipi*.bin
	rm tipi.hex

tipi.bin: $(sources)
	xas99.py -R -b -L tipi.list -o $@ rom.a99
	mv $@_4000 $@
	dd if=/dev/null of=$@ bs=1 count=0 seek=8192

tipi_emu.bin: $(sources)
	xas99.py -R -b -L tipi_emu.list -o $@ rom.a99 -D emulation nowaitwrite 
	mv $@_4000 $@

tipi.hex: tipi.bin bin2hex.py
	@ls -l tipi.bin
	python ./bin2hex.py >$@

reversed.bin: tipi.bin
	python ./binReverse.py >$@

