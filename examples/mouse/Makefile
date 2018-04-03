GAS=tms9900-as
LD=tms9900-ld
CC=tms9900-gcc
EA5SPLIT=ea5split
LIBTI99?=/home/matthew/dev/ti99/libti99

ELF2EA5=elf2ea5

FNAME=mousedemo
UCFNAME=$(shell echo -n $(FNAME) | tr 'a-z' 'A-Z')

LDFLAGS=\
  --script=linkfile

OBJECT_LIST=\
  crt0.o\
  main.o\
  tipi_msg.o\
  tipi_mouse.o\
  patterns.o

all: $(FNAME)

$(FNAME): $(FNAME).bin
	$(EA5SPLIT) $(FNAME).bin

$(FNAME).bin: $(FNAME).elf
	$(ELF2EA5) $(FNAME).elf $(FNAME).bin

$(FNAME).elf: $(OBJECT_LIST)
	$(LD) $(OBJECT_LIST) $(LDFLAGS) -L$(LIBTI99) -lti99 -o $(FNAME).elf -Map=mapfile

.phony clean:
	rm -f *.o
	rm -f *.elf
	rm -f *.bin
	rm -f *.i
	rm -f *.s
	rm -f mapfile
	rm -f patterns.h
	rm -f MOUSEDEMO

%.o: %.asm
	$(GAS) $< -o $@

%.o: %.c patterns.h tipi_mouse.h tipi_msg.h
	$(CC) -c $< -std=c99 -Os --save-temp -I$(LIBTI99) -I/home/matthew/dev/gcc-9900/lib/gcc/tms9900/4.4.0/include -o $@

patterns.h: patterns.asm
	grep "def gfx_" patterns.asm  | cut -d' ' -f2 | sed 's/^/extern const unsigned char /' | sed 's/$$/[2]\;/' >patterns.h

