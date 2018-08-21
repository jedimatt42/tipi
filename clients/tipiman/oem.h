#ifndef _OEM_H
#define _OEM_H 1

extern unsigned char PAT0;
extern unsigned char PAT127;

void defineChars();

// double line box
void drawBox2(int x1, int y1, int x2, int y2);
// single line box
void drawBox1(int x1, int y1, int x2, int y2);

// horizontal sequence of character x
void drawhline(int x, int y, char type, int length);
// vertical sequence of character x
void drawvline(int x, int y, char type, int length);

#define LEFT_T 180
#define RIGHT_T 195
#define LEFT_ARROW 17
#define RIGHT_ARROW 16

#endif