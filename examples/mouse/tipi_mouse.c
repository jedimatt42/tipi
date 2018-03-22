
#include "tipi_mouse.h"
#include "tipi_msg.h"

char mousedata[3];

#define MB_LEFT 0x01
#define MB_RIGHT 0x02
#define MB_MID 0x04

void tipiMouseRead() {
  unsigned char mousecode = 0x20;
  int readcount = 0;
  tipi_on();
  tipi_sendmsg(1, (unsigned char*)&mousecode);
  // This is assuming the linker places mousex, y, and b in sequence.
  tipi_recvmsg(&readcount, (unsigned char*)&mousedata);
  tipi_off();
}


