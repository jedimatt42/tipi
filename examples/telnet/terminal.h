#ifndef _TERMINAL
#define _TERMINAL 1

void initTerminal();

void terminalDisplay(unsigned char c);

void terminalKey(unsigned char* buf, int* len);

#endif