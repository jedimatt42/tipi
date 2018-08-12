#include "strutil.h"

#include <conio.h>
#include <string.h>

void getstr(int x, int y, char* var, int limit) {
  conio_cursorFlag = 1;
  gotoxy(x,y);
  cclear(limit);
  gotoxy(x,y);
  cputs(var);

  unsigned char normal_cursor = conio_cursorChar;

  unsigned char key = 0;
  int idx = strlen(var);
  while(key != 13) {
    // should set cursor to current char
    conio_cursorChar = var[idx];
    if (conio_cursorChar == 32 || conio_cursorChar == 0) {
      conio_cursorChar = normal_cursor;
    }
    gotoxy(x+idx,y);
    key = cgetc();
    int delidx = 0;
    switch(key) {
      case 3: // F1 - delete
        delidx = idx;
        while(var[delidx] != 0) {
          var[delidx] = var[delidx+1];
          delidx++;
        }
        delidx = strlen(var);
        var[delidx] = 0;
        gotoxy(x,y);
        cputs(var);
        cputs(" ");
        break;
      case 7: // F3 - erase line
        idx = 0;
        for(delidx = 0; delidx<limit; delidx++) {
          var[delidx] = 0;
        }
        gotoxy(x,y);
        cclear(limit-x);
        break;
      case 8: // left arrow
        if (idx > 0 && idx < limit) {
          gotoxy(x+idx,y);
          cputc(var[idx]);
          idx--;
          gotoxy(x+idx,y);
        }
        break;
      case 9: // right arrow
        if (var[idx] != 0) {
          cputc(var[idx]);
          idx++;
        }
        break;
      case 13: // return
        break;
      default: // alpha numeric
        if (key >= 32 && key <= 122) {
          gotoxy(x+idx,y);
          var[idx] = key;
          cputc(var[idx]);
          if (idx < limit) {
            idx++;
          }
        }
        break;
    }
  }
  int i=0;
  while(var[i] != 32) {
    i++;
  }
  var[i] = 0;
}


int strcmp(const char* a, const char* b) {
  int i=0;
  do {
    if (a[i] == '\0') {
      return a[i] - b[i];
    }
    i++;
  } while(a[i] == b[i]);
  return a[i] - b[i];
}

int indexof(const char* str, char c) {
  int i=0;
  while(str[i] != 0) {
    if (str[i] == c) {
      return i;
    }
    i++;
  }
  return -1;
}

int basicToCstr(const char* str, char* buf) {
  int len = (int) str[0];
  for(int i=0; i<len; i++) {
    buf[i] = str[i+1];
  }
  buf[len] = 0;
  return len;
}