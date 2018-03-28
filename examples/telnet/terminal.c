
#include "terminal.h"
#include <conio.h>
#include <string.h>

int stage;
unsigned char bytestr[20];
int bs_idx;

unsigned char cursor_store_x;
unsigned char cursor_store_y;

#define STAGE_OPEN 0
#define STAGE_ESC 1
#define STAGE_CSI 2

void resetState() {
  stage = STAGE_OPEN;
  bs_idx = 0;
}

void initTerminal() {
  cursor_store_x = 0;
  cursor_store_y = 0;

  resetState();
}

int getParamA(int def) {
  int i = 0;
  while(i<bs_idx && bytestr[i] != ';') {
    i++;
  }
  if (i == 0) {
    return def;
  }
  return atoi(bytestr);
}

int getParamB(int def) {
  int i = 0;
  while(i<bs_idx && bytestr[i] != ';') {
    i++;
  }
  // we should be pointing to beginning of param B in buffer.
  if (i == 0 || i == bs_idx) {
    return def;
  }
  unsigned char* paramb = bytestr + i + 1;
  return atoi(paramb);
}

void cursorUp(int lines) {
  int y = wherey() - lines;
  if (y < 0) {
    y = 0;
  }
  gotoy(y);
}

void cursorDown(int lines) {
  int y = wherey() + lines;
  unsigned char scx;
  unsigned char scy;
  screensize(&scx, &scy);
  scy--;
  if (y > scy) {
    y = scy;
  }
  gotoy(y);
}

void cursorRight(int cols) {
  int x = wherex() + cols;
  unsigned char scx;
  unsigned char scy;
  screensize(&scx, &scy);
  scx--;
  if (x > scx) {
    x = scx;
  }
  gotox(x);
}

void cursorLeft(int cols) {
  int x = wherex() + cols;
  if (x < 0) {
    x = 0;
  }
  gotox(x);
}

void cursorGoto(int x, int y) {
  unsigned char scx;
  unsigned char scy;
  screensize(&scx, &scy);
  if (x > scx) {
    x = scx;
  } else if (x < 1) {
    x = 1;
  }
  if (y > scy) {
    y = scy;
  } else if (y < 1) {
    y = 1;
  }
  // zero based screen
  gotox(x - 1);
  gotoy(y - 1);
}

void eraseDisplay(int opt) {
  unsigned char scx;
  unsigned char scy;
  screensize(&scx, &scy);
  int oldx = wherex();
  int oldy = wherey();
  int cursorAddr = gImage + (oldx + (oldy + scy));

  switch (opt) {
    case 0: // clear from cursor to end of screen, remain at location
      vdpmemset(cursorAddr, 0x20, (scx * scy) + gImage - cursorAddr);
      gotoxy(oldx, oldy);
      break;
    case 1: // clear from cursor to beginning of screen, remain at location
      vdpmemset(gImage, 0x20, cursorAddr - gImage);
      gotoxy(oldx, oldy);
      break;
    case 3: // TODO: if we add scroll back buffer, 3 should clear that too.
    case 2: // clear full screen, return to top
      clrscr();
      gotoxy(oldx,oldy);
      break;
  }
}

void eraseLine(int opt) {
  unsigned char scx;
  unsigned char scy;
  screensize(&scx, &scy);
  int oldx = wherex();
  int oldy = wherey();
  switch (opt) {
    case 0: // to end of line
      cclear(scx - oldx);
      break;
    case 1: // to beginning of line
      gotox(0);
      cclear(oldx);
      break;
    case 2: // entire line
      gotox(0);
      cclear(scx);
      break;
  }
  gotoxy(oldx, oldy);
}

void scrollUp(int lc) {
  gotoxy(0,23);
  for (int i = 0; i < lc; i++) {
    cputc('\n');
  }
}

void doCsiCommand(unsigned char c) {
  // Note, ANSI cursor locations (1,1) upper left corner.
  switch (c) {
    case 'A': // cursor UP, 1 param, default 1
      cursorUp(getParamA(1));
      break;
    case 'B': // cursor DOWN, 1 param, default 1
      cursorDown(getParamA(1));
      break;
    case 'C': // cursor RIGHT, 1 param, default 1
      cursorRight(getParamA(1));
      break;
    case 'D': // cursor LEFT, 1 param, default 1
      cursorLeft(getParamA(1));
      break;
    case 'E': // cursor next line, 1 param, default 1
      cursorDown(getParamA(1));
      gotox(0);
      break;
    case 'F': // cursor prev line, 1 param, default 1
      cursorUp(getParamA(1));
      gotox(0);
      break;
    case 'G': // set cursor column, 1 param, default 1
      cursorGoto(getParamA(1),wherey() + 1);
      break;
    case 'H': // set position, 2 param, defaults 1, 1
    case 'f': // synonym
      cursorGoto(getParamB(1), getParamA(1));
      break;
    case 'J': // erase in display, 1 param, default 0
      eraseDisplay(getParamA(0));
      break;
    case 'K': // erase in line, 1 param, default 0
      eraseLine(getParamA(0));
      break;
    case 'S': // scroll up lines, 1 param, default 1
      scrollUp(getParamA(1));
      break;
    case 'T': // scroll down lines, 1 param, default 1
      break;
    case 'm': // color (SGR), n params
      break;
    case 's': // store cursor, no params
      cursor_store_x = wherex();
      cursor_store_y = wherey();
      break;
    case 'u': // restore cursor, no params.
      gotoxy(cursor_store_x, cursor_store_y);
      break;
  }
}

void doEscCommand(unsigned char c) {
  
}

void charout(unsigned char ch) {
  switch (ch) {
    case '\r':
      conio_x=0;
      break;
    case '\n':
      conio_x=0;
      inc_row();
      break;
    default:
      if (ch >= ' ') {
        if (conio_x >= nTextEnd-nTextRow) {
          conio_x=0;
          inc_row();
        }
        vdpchar(conio_getvram(), ch);
        ++conio_x;
      }
    break;
  }
}

void terminalDisplay(unsigned char c) {
  if (stage == STAGE_OPEN) {
    if (c == 27) {
      stage = STAGE_ESC;
    } else {
      charout(c);
    }
  } else if (stage == STAGE_ESC) {
    if (c == '[') {
      // command begins
      stage = STAGE_CSI;
      bs_idx = 0;
      bytestr[0] = 0;
    } else {
      doEscCommand(c);
      stage = STAGE_OPEN;
    }
  } else if (stage == STAGE_CSI) { 
    if (c >= 0x40 && c <= 0x7E) {
      // command complete
      doCsiCommand(c);
      stage = STAGE_OPEN;
    } else if (c >= 0x30 && c <= 0x3F) {
      // capture params. 
      bytestr[bs_idx] = c;
      bs_idx++;
      bytestr[bs_idx] = 0;
    } else {
      // this is basically an error state... ignoring the command.
      stage = STAGE_OPEN;
    }
  }
}

void terminalKey(unsigned char* buf, int* len) {
  // translate output keys into correct terminal keyboard commands
  switch (buf[0]) {
    case 136: // ctrl-h
      buf[0] = 8; // backspace
      *len = 1;
      break;
    case 8: // left-arrrow
      buf[0] = 27; // esc
      buf[1] = 'D';
      *len = 2;
      break;
    case 11: // up-arrow
      buf[0] = 27;
      buf[1] = 'A';
      *len = 2;
      break;
    case 10: // down-arrow
      buf[0] = 27;
      buf[1] = 'B';
      *len = 2;
      break;
    case 9: // right-arrow
      buf[0] = 27;
      buf[1] = 'C';
      *len = 2;
      break;
    case 1: // tab
      buf[0] = 9;
      *len = 1;
      break;
    default:
      *len = 1;
      break;
  }
}