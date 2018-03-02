
#include <string.h>
#include <system.h>
#include <conio.h>
#include "tipi_msg.h"

#define DO 0xfd
#define WONT 0xfc
#define WILL 0xfb
#define DONT 0xfe
#define CMD 0xff
#define CMD_ECHO 1
#define CMD_WINDOW_SIZE 31

unsigned char hostname[32];
unsigned char port[10];

unsigned char buffer[128];
unsigned char output[10];

// state machine variables
int mode;
unsigned char command;
unsigned char param;

#define TI_SOCKET_REQUEST 0x22
#define TI_SOCKET_OPEN 0x01
#define TI_SOCKET_CLOSE 0x02
#define TI_SOCKET_WRITE 0x03
#define TI_SOCKET_READ 0x04
#define socketId 0x00

void clearbuf(int len, unsigned char *buf) {
  for (int i=0; i<len; i++) {
    buf[i] = 0;
  }
}

void setupScreen() {
  set_text();
  charsetlc();
  bgcolor(COLOR_CYAN);
  textcolor(COLOR_BLACK);
  clrscr();
  gotoxy(0,0);
  cputs("1: 40 Column");
  gotoxy(0,1);
  cputs("2: 80 Column");
  while(1) {
    unsigned char key = cgetc();
    if (key == 50) {
      set_text80();
      charsetlc();
      clrscr();
      return;
    } else if (key == 49) {
      set_text();
      charsetlc();
      clrscr();
      return;
    }
  }
}

void getstr(int x, int y, unsigned char* var, int maxlen) {
  gotoxy(x,y);
  cclear(40-x);
  gotoxy(x,y);
  cputs(var);

  unsigned char key = 0;
  int idx = strlen(var);
  while(key != 13) {
    // should set cursor to current char
    conio_cursorChar = var[idx];
    if (conio_cursorChar == 32 || conio_cursorChar == 0) {
      conio_cursorChar = 30;
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
  int i=0;
  while(var[i] != 32) {
    i++;
  }
  var[i] = 0;
}

unsigned char connect(unsigned char* hostname, unsigned char* port) {
  buffer[0] = TI_SOCKET_REQUEST;
  buffer[1] = socketId;
  buffer[2] = TI_SOCKET_OPEN;
  unsigned char* cursor = buffer + 3;
  strcpy(cursor, hostname);
  cursor += strlen(hostname);
  *cursor = ':';
  cursor++;
  strcpy(cursor, port);
  cursor += strlen(port);
  int bufsize = cursor - buffer;

  tipi_on();
  tipi_sendmsg(bufsize, buffer);
  bufsize = 0;
  tipi_recvmsg(&bufsize, buffer);
  tipi_off();

  return buffer[0];
}

int send_char(unsigned char byte) {
  output[0] = TI_SOCKET_REQUEST;
  output[1] = socketId;
  output[2] = TI_SOCKET_WRITE;
  output[3] = byte;
  tipi_on();
  tipi_sendmsg(4, output);
  int bufsize = 0;
  tipi_recvmsg(&bufsize, buffer);
  tipi_off();
  return buffer[0];
}

int send_cmd(unsigned char req, unsigned char param) {
  output[0] = TI_SOCKET_REQUEST;
  output[1] = socketId;
  output[2] = TI_SOCKET_WRITE;
  output[3] = CMD;
  output[4] = req;
  output[5] = param;
  tipi_on();
  tipi_sendmsg(6, output);
  int bufsize = 0;
  tipi_recvmsg(&bufsize, buffer);
  tipi_off();
  return buffer[0];
}

int read_socket() {
  output[0] = TI_SOCKET_REQUEST;
  output[1] = socketId;
  output[2] = TI_SOCKET_READ;
  output[3] = 0; // buffer size is just 128 bytes.
  output[4] = 128;
  tipi_on();
  tipi_sendmsg(5, output);
  int bufsize = 0;
  tipi_recvmsg(&bufsize, buffer);
  tipi_off();
  return bufsize;
}

void clearState() {
  mode = 0;
  command = 0;
  param = 0;
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
        cputc(current);
      }
    }
  }
}

void term() {
  setupScreen();
  clearState();
  clearbuf(32, hostname);
  clearbuf(10, port);
  clearbuf(128, buffer);
  setupScreen();
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
    __asm__("limi 2\n\tlimi 0");

    if (kbhit()) {
      unsigned char key = cgetc();
      // cputc(key);
      if (!send_char(key)) {
        cputs("Disconnected. Press any key.");
        cgetc();
	return;
      }
      idle = 0;
    } else {
      idle++;
      if (idle > 100) {
        int bufsize = read_socket();
        process(bufsize, buffer);
      }
    }  
  }
}

void main() {
  while( 1 ) {
    term();
  }
}


