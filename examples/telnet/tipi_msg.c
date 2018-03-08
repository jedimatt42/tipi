#include "tipi_msg.h"

void tipi_on()
{
  TIPI_ON;
}

void tipi_off()
{
  TIPI_OFF;
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

