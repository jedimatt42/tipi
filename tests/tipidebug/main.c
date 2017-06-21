
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
  VDP_SET_REGISTER(VDP_REG_MODE1, unblank);
  writestring(1, 0, "TIPI Debug");

  tipi_on();

  writestring(2, 4, "echo TIPI");

  buffer[10] = 'T';
  buffer[11] = 'I';
  buffer[12] = 'P';
  buffer[13] = 'I';

  int inc = 0;
  int counter = 0;

  while(1) {

    VDP_WAIT_VBLANK_CRU;
    counter++;
    if (counter % 15 == 0) {
      tipi_sendmsg(4, buffer+10);
      tipi_recvmsg(&count, buffer);
      buffer[count] = 0;
      writebytehex(3, 4, buffer[0]);
      writebytehex(3, 7, buffer[1]);
      writebytehex(3, 10, buffer[2]);
      writebytehex(3, 13, buffer[3]);

      inc++;
      buffer[10] = 'T' + inc & 0xFF;
      buffer[11] = 'I' + inc & 0xFF;
      buffer[12] = 'P' + inc & 0xFF;
      buffer[13] = 'I' + inc & 0xFF;
    }
  }

  tipi_off();

  halt();
}
