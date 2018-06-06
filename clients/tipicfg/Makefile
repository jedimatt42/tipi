GAS=tms9900-as
LD=tms9900-ld
CC=tms9900-gcc
EA5SPLIT=ea5split
LIBTI99?=/home/matthew/dev/ti99/libti99

ELF2EA5=elf2ea5

FNAME=tipicfg
UCFNAME=$(shell echo -n $(FNAME) | tr 'a-z' 'A-Z')

LDFLAGS=\
  --script=linkfile

OBJECT_LIST=\
  crt0.o\
  main.o

all: $(FNAME)

$(FNAME): $(FNAME).bin
	$(EA5SPLIT) $(FNAME).bin
	cp TIPICF? ../../setup/bin/

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
	rm -f TIPICF?

%.o: %.asm
	$(GAS) $< -o $@

%.o: %.c
	$(CC) -c $< -std=c99 -Os --save-temp -I$(LIBTI99) -I/home/matthew/dev/gcc-9900/lib/gcc/tms9900/4.4.0/include -o $@

