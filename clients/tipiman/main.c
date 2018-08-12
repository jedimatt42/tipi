
#include "dsrutil.h"
#include "strutil.h"
#include "oem.h"

#define DSR_STATUS_EOF DST_STATUS_EOF

#include <string.h>
#include <conio.h>
#include <system.h>


#define GPLWS ((unsigned int*)0x83E0)
#define DSRTS ((unsigned char*)0x401A)

#define TIPIMAN_VER "1"

char ldrive[30];

void initGlobals() {
  strcpy(ldrive, "DSK2.");
}

void setupScreen() {
  set_text80();
  defineChars();
  bgcolor(COLOR_CYAN);
  textcolor(COLOR_BLACK);
}

void layoutScreen() {
  clrscr();
  gotoxy(0,0);
  cputs("TIPIMAN v");
  cputs(TIPIMAN_VER);
  drawBox(0, 1, 39, 3);
  drawBox(0, 4, 39, 22);
  drawBox(40, 1, 79, 3);
  drawBox(40, 4, 79, 22);
}

int entry_row = 0;

int lCatRecord(char* buf) {
  if (entry_row == 0) {
    entry_row++;
    return 0;
  }
  char cstr[11];
  basicToCstr(buf, cstr);
  cputsxy(2, 4 + entry_row++, cstr);
  return 0;
}

void main()
{
  initGlobals();
  setupScreen();

  layoutScreen();
  gotoxy(1,2);
  cputs("SRC:");
  cputs(ldrive);
  gotoxy(41,2);
  cputs("DST:");
  getstr(5,2, ldrive, 30);
  entry_row = 0;
  loadDir(ldrive, &lCatRecord);

  halt();
}

