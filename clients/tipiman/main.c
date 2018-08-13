
#include "dsrutil.h"
#include "strutil.h"
#include "oem.h"
#include "tifloat.h"

#define DSR_STATUS_EOF DST_STATUS_EOF

#include <string.h>
#include <conio.h>
#include <system.h>


#define GPLWS ((unsigned int*)0x83E0)
#define DSRTS ((unsigned char*)0x401A)

#define TIPIMAN_VER "1"

int entry_row = 0;

struct __attribute__((__packed__)) DirEntry {
  char name[11];
  int type;
  int sectors;
  int reclen;
}; 

struct DirEntry lentries[200];
char lvolname[11];
int llen = 0;
int lfree = 0;
char ldrive[30];

const char* const ftypes[] = {
  "D/F",
  "D/V",
  "I/F",
  "I/V",
  "PRG",
  "DIR"
};


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

  gotoxy(1,2);
  cputs("SRC:");
  cputs(ldrive);
  gotoxy(41,2);
  cputs("DST:");
}

void drawLentries(int start) {
  int done = 0;
  for(int i=0;i<17;i++) {
    gotoxy(1, 5+i);
    cclear(38);
    struct DirEntry* entry = &(lentries[i+start]);
    if (!done && entry->name[0] != 0) {
      gotoxy(2, 5+i);
      cputs(entry->name);
      gotoxy(13, 5+i);
      cputs(ftypes[entry->type - 1]);
      if (entry->type < 4) {
        gotoxy(17, 5+i);
        cputs(int2str(entry->reclen));
      }
    } else {
      done = 1;
    }
  }
}

int lCatRecord(char* buf) {
  char cstr[11];
  int namlen = basicToCstr(buf, cstr);
  int a = ti_floatToInt(buf+1+namlen);
  int j = ti_floatToInt(buf+10+namlen);
  int k = ti_floatToInt(buf+19+namlen);
  if (entry_row == 0) {
    strcpy(lvolname, cstr);
    lfree = k;
  } else {
    struct DirEntry* entry = &(lentries[entry_row-1]);
    strcpy(entry->name, cstr);
    entry->type = a;
    entry->sectors = j;
    entry->reclen = k;
  }
  entry_row++;
  return 0;
}

void catalogLdrive() {
  entry_row = 0;
  loadDir(ldrive, &lCatRecord);
  lentries[entry_row].name[0] = 0;
  drawLentries(0);
}

void main()
{
  initGlobals();
  setupScreen();
  layoutScreen();

  while(1) {
    getstr(5,2, ldrive, 30);
    catalogLdrive();
  }
}

