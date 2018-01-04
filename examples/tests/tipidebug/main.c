
#include <vdp.h>
#include <system.h>
#include "tipi_msg.h"

#define SCREEN_COLOR (COLOR_BLACK << 4) + COLOR_CYAN
#define ERROR_COLOR (COLOR_BLACK << 4) + COLOR_MEDRED
#define SUCCESS_COLOR (COLOR_BLACK << 4) + COLOR_LTGREEN

void writebytehex(unsigned int row, unsigned int col, const unsigned char value) {
  unsigned char buf[3] = { 0, 0, 0 };
  *((unsigned int*)buf) = byte2hex[value];
  writestring(row, col, buf);
}

inline void call_clear()
{
  vdpmemset(0x0000,' ',nTextEnd);
}

inline void vdp_lock()
{
  VDP_INT_DISABLE;
}

inline void vdp_release()
{
  VDP_INT_ENABLE;
}

void main()
{
  unsigned int count = 0;
  unsigned int* cptr = (unsigned int*)&count;
  // I have moved the stack down, and left this 256 byte buffer in low-expmem
  unsigned char* buffer = (unsigned char*) 0x2000;
  vdp_lock();
  int unblank = set_text();
  VDP_SET_REGISTER(VDP_REG_COL, SCREEN_COLOR);
  call_clear();
  charsetlc();
  writestring(1, 0, "TIPI Debug");

  VDP_SET_REGISTER(VDP_REG_MODE1, unblank);

  tipi_on();

  buffer[10] = 1;
  buffer[11] = 2;
  buffer[12] = 3;
  buffer[13] = 4;
  buffer[14] = 5;
  buffer[15] = 6;

  int counter = 0;

  while(1) {

    VDP_WAIT_VBLANK_CRU;
    counter++;
    if (counter % 5 == 0) {
      tipi_sendmsg(6, buffer+10);
      tipi_recvmsg(&count, buffer);
      buffer[count] = 0;
      writebytehex(3, 4, buffer[0]);
      writebytehex(3, 7, buffer[1]);
      writebytehex(3, 10, buffer[2]);
      writebytehex(3, 13, buffer[3]);
      writebytehex(3, 16, buffer[4]);
      writebytehex(3, 19, buffer[5]);

      buffer[10] += 1;
      buffer[11] += 1;
      buffer[12] += 1;
      buffer[13] += 1;
      buffer[14] += 1;
      buffer[15] += 1;
    }
  }

  tipi_off();

  halt();
}
