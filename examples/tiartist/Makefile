
default: all

all: TIPIM

clean:
	rm -fr *.o TIPIM

%.o: %.a99
	xas99.py -R -C -o $@ $<

TIPIM: tipim.o
	xdm99.py -t -T $< -o TIPIM -f DIS/FIX80

