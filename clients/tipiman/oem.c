#include "oem.h"
#include <conio.h>

void defineChars() {
  charsetlc();
  vdpmemcpy(gPattern, &PAT0, 32 * 8);
  vdpmemcpy(gPattern + (127 * 8), &PAT127, 129 * 8);
  conio_cursorChar = 219;
}


void drawBox(int x1, int y1, int x2, int y2) {
  int span = x2 - x1 - 1;
  int lank = y2 - y1 - 1;
  cputcxy(x1, y1, 201);
  vdpmemset(conio_getvram(), 205, x2 - x1 - 1);
  cputcxy(x2, y1, 187);
  cputcxy(x1, y2, 200);
  vdpmemset(conio_getvram(), 205, x2 - x1 - 1);
  cputcxy(x2, y2, 188);
  gotoxy(x1, y1+1);
  int addr = conio_getvram();
  for(int i=0; i<lank; i++) {
    vdpchar(addr + (i * 80), 186);
  }
  gotoxy(x2, y1+1);
  addr = conio_getvram();
  for(int i=0; i<lank; i++) {
    vdpchar(addr + (i * 80), 186);
  }
}