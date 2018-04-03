
#include <string.h>
#include <system.h>
#include <conio.h>

int crubase;

#define DSRTS ((unsigned char*)0x401A)

// should act like memory
#define TDOUT ((volatile unsigned char*)0x5FFF)
#define TCOUT ((volatile unsigned char*)0x5FFD)
// don't know how to self test these yet...
#define RDIN  ((volatile unsigned char*)0x5FFB)
#define RCIN  ((volatile unsigned char*)0x5FF9)

void enableTipi() {
  __asm__("mov %0,r12\n\tsbo 0" : : "r"(crubase) : "r12");
}

void disableTipi() {
  __asm__("mov %0,r12\n\tsbz 0" : : "r"(crubase) : "r12");
}

void discoverCrubase() {
  crubase = 0x1000;
  while(crubase < 0x2000) {
    enableTipi();
    int* cursor = (int*)0x4000;
    if (0xAA01 == *cursor) {
      cursor = (int*)0x4008; // standard location for dsr link list in rom header.
      if (0x0000 != *cursor) {
	cursor = (int*)*cursor; // now 1st entry in dsr list.
	cursor += 2; // points to first dsr name length
	unsigned char* bytes = (unsigned char*)cursor;
	if (bytes[0] == 4 && 
            bytes[1] == 'T' &&
	    bytes[2] == 'I' &&
	    bytes[3] == 'P' &&
	    bytes[4] == 'I') {
	  disableTipi();
	  return;
	}
      }
    }
    disableTipi();
    crubase += 0x0100;
  }
  crubase = 0x0000;
}

void printDsrTimestamp() {
  if (crubase != 0) {
    enableTipi();
    // copy from the ROM to screen
    if (*(DSRTS) == '2') { // good for almost 100 years
      cputs(DSRTS);
    }
    disableTipi();
  }
}

void testROM() {
  printDsrTimestamp();
  cputs("\n");
}

void testOutputRegisters() {
  int tderrors = 0;
  cputs("\nTesting TDOUT...\n");
  enableTipi();
  for(int i = 0; i<=255; i++) {
    *TDOUT = i;
    unsigned char x = *TDOUT;
    if (x != i) {
      cputs("TDOUT error for value: ");
      cputs(uint2str(i));
      cputs(", found: ");
      cputs(uint2str(x));
      cputs("\n");
      tderrors++;
    }
  }
  disableTipi();

  int tcerrors = 0;
  cputs("\nTesting TCOUT...\n");
  enableTipi();
  for(int i = 0; i<=255; i++) {
    *TCOUT = i;
    unsigned char x = *TCOUT;
    if (x != i) {
      cputs("TCOUT error for value: ");
      cputs(uint2str(i));
      cputs(", found: ");
      cputs(uint2str(x));
      cputs("\n");
      tcerrors++;
    }
  }
  disableTipi();

  if (tderrors > 0) {
    cputs("\nErrors retaining value in TDOUT register\n");
  }
  if (tcerrors > 0) {
    cputs("\nErrors retaining value in TCOUT register\n");
  }
}

void testInputRegisters() {
}

void setupScreen() {
  set_text();
  charset();
  bgcolor(COLOR_CYAN);
  textcolor(COLOR_BLACK);
}

unsigned char pressAnyKey() {
  while( 1 ) {
    if (kbhit()) {
      unsigned char k = cgetc();
      return k;
    }
  }
}

void main()
{
  setupScreen();

  clrscr();
  gotoxy(0,23);
  cputs("TIPI Diagnostics\n\n");
  discoverCrubase();
  cputs("CRU base: ");
  cputs(uint2str(crubase));
  if (crubase == 0) {
    cputs("..error detecting TIPI\nset CRUBASE to default(0x1000)\n");
    cputs("press any key to continue");
    pressAnyKey();
    crubase = 0x1000;
  }
  cputs("\n");
  testROM();
  cputs("\nDoes date look good?");
  if (pressAnyKey() == 'Y') {
    testOutputRegisters();
    testInputRegisters();
  }

  cputs("testing complete...");
  pressAnyKey();
  __asm__("BLWP @0x0000");
}

