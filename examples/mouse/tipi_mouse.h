#ifndef _tipi_mouse
#define _tipi_mouse

extern char mousedata[3];

#define mousex mousedata[0]
#define mousey mousedata[1]
#define mouseb mousedata[2]

#define MB_LEFT 0x01
#define MB_RIGHT 0x02
#define MB_MID 0x04

void tipiMouseRead();

#endif

