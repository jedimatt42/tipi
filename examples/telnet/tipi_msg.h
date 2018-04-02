#ifndef _tipi_msg_h
#define _tipi_msg_h 1



void tipi_on();

void tipi_off();

void tipi_recvmsg(unsigned int* len, unsigned char* buf);

void tipi_sendmsg(unsigned int len, const unsigned char* buf);

#endif
