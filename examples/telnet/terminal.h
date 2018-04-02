#ifndef _terminal_h
#define _terminal_h 1

void initTerminal();
void terminalDisplay(unsigned char c);
void terminalKey(unsigned char* buf, int* len);

extern int termWidth;

void resetState();
int getParamA(int def);
int getParamB(int def);
void cursorUp(int lines);
void cursorDown(int lines);
void cursorRight(int cols);
void cursorLeft(int cols);
void cursorGoto(int x, int y);
void eraseDisplay(int opt);
void eraseLine(int opt);
void scrollUp(int lc);
void sendTermCoord();
void sendTermType();
void setColors();
void doSGRCommand();
void doCsiCommand(unsigned char c);
int doEscCommand(unsigned char c);
void charout(unsigned char ch);

#endif
