
#include <vdp.h>
#include <system.h>

#define SCREEN_COLOR (COLOR_BLACK << 4) + COLOR_CYAN
#define ERROR_COLOR (COLOR_BLACK << 4) + COLOR_MEDRED
#define SUCCESS_COLOR (COLOR_BLACK << 4) + COLOR_LTGREEN

#define TI_DATA *((volatile unsigned char*)0x5fff) 
#define TI_CONTROL *((volatile unsigned char*)0x5ffd) 
#define RPI_DATA *((volatile unsigned char*)0x5ffb) 
#define RPI_CONTROL *((volatile unsigned char*)0x5ff9) 

#define ACK_MASK 0x03
#define SYN_BIT 0x02
#define RESET 0x01
#define DIR_REQUEST_BYTE 0x04

void writebytehex(unsigned int row, unsigned int col, const unsigned char value) {
  unsigned char buf[3] = { 0, 0, 0 };
  *((unsigned int*)buf) = byte2hex[value];
  writestring(row, col, buf);
}

void main()
{
  int unblank = set_text();
  VDP_SET_REGISTER(VDP_REG_COL, SCREEN_COLOR);
  vdpmemset(0x0000,' ',nTextEnd);
  charsetlc();
  VDP_SET_REGISTER(VDP_REG_MODE1, unblank);

  __asm__("li r12, >1000\n\tsbo 0");

  writestring(1, 0, "TIPI Debug");
  writestring(3, 4, "RC  RD");

  while(1) {
    int i = 4;
    while(i < 20) {
      writestring(i, 2, ">");
      writebytehex(i, 4, RPI_CONTROL);
      writebytehex(i, 8, RPI_DATA);
      writestring(i, 2, " ");
      i++;
    }
    __asm__("limi 2\n\tlimi 0");
  }

  __asm__("limi2");

  halt();
}
