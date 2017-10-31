#ifndef _tipi_msg
#define _tipi_msg


#define GPLWS_R0 *((volatile unsigned int*)0x83E0) 
#define GPLWS_R1 *((volatile unsigned int*)0x83E2) 

#define TIPI_ON __asm__("li r12, >1000\n\tsbo 0")
#define TIPI_OFF __asm__("li r12, >1000\n\tsbz 0")

void tipi_on();

void tipi_off();

void tipi_recvmsg(unsigned int* len, unsigned char* buf);

void tipi_sendmsg(unsigned int len, const unsigned char* buf);

#endif
