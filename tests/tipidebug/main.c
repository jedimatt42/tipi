
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

#define GPLWS_R0 *((volatile unsigned int*)0x83E0) 
#define GPLWS_R1 *((volatile unsigned int*)0x83E2) 

void writebytehex(unsigned int row, unsigned int col, const unsigned char value) {
  unsigned char buf[3] = { 0, 0, 0 };
  *((unsigned int*)buf) = byte2hex[value];
  writestring(row, col, buf);
}

void recvmsg(unsigned int* len, unsigned char* buf)
{
  GPLWS_R0 = (unsigned int)len;
  GPLWS_R1 = (unsigned int)buf;
  __asm__("blwp @>4010");
  *len = GPLWS_R0;
}

void sendmsg(unsigned int len, const unsigned char* buf)
{
  GPLWS_R0 = len;
  GPLWS_R1 = (unsigned int)buf;
  __asm__("blwp @>4014");
}

inline void call_clear()
{
  vdpmemset(0x0000,' ',nTextEnd);
}

inline void vdp_lock()
{
  __asm__("limi 0");
}

inline void vdp_release()
{
  __asm__("limi 2");
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

  __asm__("li r12, >1000\n\tsbo 0");


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
      sendmsg(4, buffer+10);
      recvmsg(&count, buffer);
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

  __asm__("li r12, >1000\n\tsbz 0");

  halt();
}
