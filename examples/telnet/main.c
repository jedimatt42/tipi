
#include <string.h>
#include <system.h>
#include <conio.h>
#include "ti_socket.h"
#include "terminal.h"

extern unsigned char PAT0;
extern unsigned char PAT127;

#define DO 0xfd
#define WONT 0xfc
#define WILL 0xfb
#define DONT 0xfe
#define CMD 0xff
#define CMD_ECHO 1
#define CMD_WINDOW_SIZE 31

unsigned char hostname[32];
unsigned char port[10];


// state machine variables
int mode;
unsigned char command;
unsigned char param;


void clearbuf(int len, unsigned char *buf) {
  for (int i=0; i<len; i++) {
    buf[i] = 0;
  }
}

void defineChars() {
  charsetlc();
  vdpmemcpy(gPattern, &PAT0, 32 * 8);
  vdpmemcpy(gPattern + (127 * 8), &PAT127, 129 * 8);
  conio_cursorChar = 219;
}

void setupScreen() {
  VDP_SET_REGISTER(0x32, 0x80);
  VDP_SET_REGISTER(0x02, 0x00);
  set_graphics(0);
  set_text();
  defineChars();
  bgcolor(COLOR_BLACK);
  textcolor(COLOR_GRAY);
  clrscr();
  cursor(1);
  gotoxy(0,0);
  cputs("1: 40 Column");
  gotoxy(0,1);
  cputs("2: 80 Column");
  int waiting = 1;
  while(waiting) {
    VDP_INT_POLL;
    if (kbhit()) {
      unsigned char key = cgetc();
      if (key == 50) {
        set_text80_color();
        waiting = 0;
      } else if (key == 49) {
        set_text();
        waiting = 0;
      }
    }
  }
  defineChars();
  clrscr();
}

void getstr(int x, int y, unsigned char* var, int maxlen) {
  gotoxy(x,y);
  cclear(40-x);
  gotoxy(x,y);
  cputs(var);

  unsigned char normal_cursorChar = conio_cursorChar;
  conio_cursorFlag = 1;
  unsigned char key = 0;
  int idx = strlen(var);
  while(key != 13) {
    // should set cursor to current char
    conio_cursorChar = var[idx];
    if (conio_cursorChar == 32 || conio_cursorChar == 0) {
      conio_cursorChar = normal_cursorChar;
    }
    gotoxy(x+idx,y);
    VDP_INT_POLL;
    if (1 || kbhit()) {
      key = cgetc();
      int delidx = 0;
      switch(key) {
        case 3: // F1 - delete
          delidx = idx;
          while(var[delidx] != 0) {
            var[delidx] = var[delidx+1];
            delidx++;
          }
          delidx = strlen(var) - 1;
          var[delidx] = 0;
          gotoxy(x,y);
          cputs(var);
          break;
        case 7: // F3 - erase line
          var[idx] = 0;
          delidx = idx + 1;
          while(var[delidx] != 0) {
            var[delidx] = 0;
            delidx++;
          }
          gotoxy(x+idx,y);
          cclear(40-(x+idx));
          break;
        case 8: // left arrow
          if (idx > 0) {
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
            if (idx == maxlen) {
              idx--;
            }
          }
          break;
        case 13: // return
          break;
        default: // alpha numeric
          if (key >= 32 && key <= 122) {
            var[idx++] = key;
            cputc(key);
            if (idx == maxlen) {
              idx--;
            }
          }
      }
    }
  }
  int i=0;
  while(var[i] != 32) {
    i++;
  }
  var[i] = 0;
}

int send_cmd(unsigned char req, unsigned char param) {
  unsigned char cmdbuf[3];
  cmdbuf[0] = CMD;
  cmdbuf[1] = req;
  cmdbuf[2] = param;
  return send_chars(cmdbuf, 3);
}

void clearState() {
  mode = 0;
  command = 0;
  param = 0;
  initTerminal();
}

void process(int bufsize, unsigned char* buffer) {
  for(int i=0; i<bufsize; i++) {
    unsigned char current = buffer[i];
    if (mode == CMD) {
      if (command == 0) {
        command = current;
      } else {
        switch (command) {
          case DO:
            send_cmd(WONT, current);
            break;
          case DONT:
            send_cmd(WONT, current);
            break;
          case WILL:
            break;
          case WONT:
            break;
          default:
            break;
        }
        clearState();
      }
    } else {
      if (current == CMD) {
        mode = CMD;
      } else {
        terminalDisplay(current);
      }
    }
  }
}

unsigned blinkenLights = 0;

void unblink() {
  if (conio_cursorChar != 0) {
    vdpchar(conio_getvram(), conio_cursorChar);
    conio_cursorChar = 0;
  }
}

void blink() {
  if ((blinkenLights % 100) < 50) {
    if (conio_cursorChar == 0) {
      int here = conio_getvram();
      VDP_SET_ADDRESS(here);
      __asm__("NOP");
      conio_cursorChar = VDPRD;
      vdpchar(here, 219);
    }
  } else {
    unblink();
  }
}

void term() {
  setupScreen();
  clearState();
  clearbuf(32, hostname);
  clearbuf(10, port);
  gotoxy(0,0);
  cputs("HOST: ");
  getstr(6,0, hostname, 32);
  gotoxy(6,0);
  cputs(hostname);
  gotoxy(0,1);
  cputs("PORT: ");
  getstr(6,1, port, 10);
  gotoxy(6,1);
  cputs(port);

  conio_cursorFlag = 0;
  conio_cursorChar = 219;

  unsigned char result = connect(hostname, port);
  if (result != 255) {
    gotoxy(0,3);
    cputs("Error connecting");
    gotoxy(0,4);
    cputs("Press any key to continue...");
    cgetc();
    return;
  } else {
    gotoxy(0,3);
    cputs("Connected.");
    gotoxy(0,4);
  }

  int idle = 0;

  while( 1 ) {
    VDP_INT_POLL;

    if (kbhit()) {
      // terminal may need to transform this to
      // multiple characters.
      unsigned char keybuf[4];
      keybuf[0] = cgetc();
      int keylen = 1;
      terminalKey(keybuf, &keylen);
      if (!send_chars(keybuf, keylen)) {
        cputs("Disconnected. Press any key.");
        cgetc();
        return;
      }
      idle = 0;
      blinkenLights = 0;
    } else {
      idle++;
      blinkenLights++;
      if (idle > 300) {
        int bufsize = read_socket();
        if (bufsize) {
          blinkenLights = 0;
          unblink();
          process(bufsize, buffer);
        } else {
          blink();
        }
      }
    }  
  }
}

void main() {
  while( 1 ) {
    term();
  }
}


