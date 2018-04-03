#include "tipi_msg.h"


#define GPLWS_R0 *((volatile unsigned int*)0x83E0) 
#define GPLWS_R1 *((volatile unsigned int*)0x83E2) 

void tipi_lib_init();

int tipi_crubase = 0;

inline void enableTipi() {
  __asm__("mov %0,r12\n\tsbo 0" : : "r"(tipi_crubase) : "r12");
}

inline void disableTipi() {
  __asm__("mov %0,r12\n\tsbz 0" : : "r"(tipi_crubase) : "r12");
}

void tipi_on()
{
  if (tipi_crubase == 0) {
    tipi_lib_init();
  }
  enableTipi();
}

void tipi_off()
{
  disableTipi();
}

void tipi_lib_init()
{
  tipi_crubase = 0x1000;
  while(tipi_crubase < 0x2000) {
    enableTipi();
    unsigned int* dsrrom = (unsigned int*) 0x4000;
    dsrrom += 4; // 4 words, not bytes
    
    if (*dsrrom != 0) {
      dsrrom = ((unsigned int*) *dsrrom) + 2;
      unsigned char* dsrname = (unsigned char*) dsrrom;
      // TIPI will always have device TIPI first in dsrlnk list.
      if (dsrname[0] == 4 && dsrname[1] == 'T' && dsrname[2] == 'I' && dsrname[3] == 'P' && dsrname[4] == 'I') {
        disableTipi();
        return;
      }
    }
    disableTipi();
    tipi_crubase += 0x0100;
  }
  tipi_crubase = 0x0000;
}

void tipi_recvmsg(unsigned int* len, unsigned char* buf)
{
  GPLWS_R0 = (unsigned int)*len;
  GPLWS_R1 = (unsigned int)buf;
  __asm__("lwpi >83E0\n\tmov @>4010,r4\n\tbl *r4\n\tlwpi >8300");
  *len = GPLWS_R0;
}

void tipi_sendmsg(unsigned int len, const unsigned char* buf)
{
  GPLWS_R0 = len;
  GPLWS_R1 = (unsigned int)buf;
  __asm__("lwpi >83E0\n\tmov @>4012,r4\n\tbl *r4\n\tlwpi >8300");
}

