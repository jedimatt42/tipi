
#define GPLWS_R0 *((volatile unsigned int*)0x83E0) 
#define GPLWS_R1 *((volatile unsigned int*)0x83E2) 

#define TIPI_ON __asm__("li r12, >1000\n\tsbo 0")
#define TIPI_OFF __asm__("li r12, >1000\n\tsbz 0")

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
  GPLWS_R0 = (unsigned int)len;
  GPLWS_R1 = (unsigned int)buf;
  __asm__("blwp @>4010");
  *len = GPLWS_R0;
}

void tipi_sendmsg(unsigned int len, const unsigned char* buf)
{
  GPLWS_R0 = len;
  GPLWS_R1 = (unsigned int)buf;
  __asm__("blwp @>4014");
}

