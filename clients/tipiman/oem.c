#include "oem.h"
#include <conio.h>

void defineChars() {
  charsetlc();
  vdpmemcpy(gPattern, &PAT0, 32 * 8);
  vdpmemcpy(gPattern + (127 * 8), &PAT127, 129 * 8);
  conio_cursorChar = 219;
}


// horizontal sequence of character x
void drawhline(int x, int y, char type, int length) {
  gotoxy(x, y);
  vdpmemset(conio_getvram(), type, length);
}

// vertical sequence of character x
void drawvline(int x, int y, char type, int length) {
  gotoxy(x, y);
  int addr = conio_getvram();
  for(int i=0; i<length; i++) {
    vdpchar(addr + (i * 80), type);
  }
}

#define SINGLE_VERTICAL 179
#define SINGLE_TOP_RIGHT 191
#define SINGLE_BOTTOM_RIGHT 217
#define SINGLE_BOTTOM_LEFT 192
#define SINGLE_TOP_LEFT 218
#define SINGLE_HORIZONTAL 196

#define DOUBLE_VERTICAL 186
#define DOUBLE_TOP_RIGHT 187
#define DOUBLE_BOTTOM_RIGHT 188
#define DOUBLE_BOTTOM_LEFT 200
#define DOUBLE_TOP_LEFT 201
#define DOUBLE_HORIZONTAL 205

void drawBox2(int x1, int y1, int x2, int y2) {
  int span = x2 - x1 - 1;
  int lank = y2 - y1 - 1;
  cputcxy(x1, y1, DOUBLE_TOP_LEFT);
  vdpmemset(conio_getvram(), DOUBLE_HORIZONTAL, x2 - x1 - 1);
  cputcxy(x2, y1, DOUBLE_TOP_RIGHT);
  cputcxy(x1, y2, DOUBLE_BOTTOM_LEFT);
  vdpmemset(conio_getvram(), DOUBLE_HORIZONTAL, x2 - x1 - 1);
  cputcxy(x2, y2, DOUBLE_BOTTOM_RIGHT);
  drawvline(x1, y1+1, DOUBLE_VERTICAL, lank);
  drawvline(x2, y1+1, DOUBLE_VERTICAL, lank);
  gotoxy(x2, y2);
  vdpmemset(conio_getvram(), DOUBLE_BOTTOM_RIGHT, 1);
}

// single line box
void drawBox1(int x1, int y1, int x2, int y2) {
  int span = x2 - x1 - 1;
  int lank = y2 - y1 - 1;
  cputcxy(x1, y1, SINGLE_TOP_LEFT);
  vdpmemset(conio_getvram(), SINGLE_HORIZONTAL, x2 - x1 - 1);
  cputcxy(x2, y1, SINGLE_TOP_RIGHT);
  cputcxy(x1, y2, SINGLE_BOTTOM_LEFT);
  vdpmemset(conio_getvram(), SINGLE_HORIZONTAL, x2 - x1 - 1);
  drawvline(x1, y1+1, SINGLE_VERTICAL, lank);
  drawvline(x2, y1+1, SINGLE_VERTICAL, lank);
  gotoxy(x2, y2);
  vdpmemset(conio_getvram(), SINGLE_BOTTOM_RIGHT, 1);
}
