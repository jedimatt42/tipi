GAS=tms9900-as
LD=tms9900-ld
CC=tms9900-gcc
LIBTI99?=/home/matthew/dev/ti99/libti99

ELF2CART=elf2cart

FNAME=mouseTest

LDFLAGS=\
  --section-start .text=6000 --section-start .data=2000

OBJECT_LIST=\
  header.o\
  crt0.o\
  patterns.o\
  tipi_msg.o\
  tipi_mouse.o\
  main.o

all: $(FNAME).bin

$(FNAME).bin: $(FNAME).elf
	$(ELF2CART) $(FNAME).elf $(FNAME).bin

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

patterns.h: patterns.asm
	grep "def gfx_" patterns.asm  | cut -d' ' -f2 | sed 's/^/extern const unsigned char /' | sed 's/$$/[2]\;/' >patterns.h

%.o: %.asm
	$(GAS) $< -o $@

%.o: %.c patterns.h tipi_mouse.h tipi_msg.h
	$(CC) -c $< -std=c99 -O2 --save-temp -I$(LIBTI99) -o $@

