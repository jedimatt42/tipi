#ifndef _ti_socket_h
#define _ti_socket_h 1

extern unsigned char buffer[512];

unsigned char connect(unsigned char* hostname, unsigned char* port);

// will send at most 122 byte character sequences (cause size of output buffer)
int send_chars(unsigned char* buf, int size);

int read_socket();

#endif
