#ifndef _main_h
#define _main_h 1

void clearbuf(int len, unsigned char *buf);
void defineChars();
void setupScreen() ;{
void getstr(int x, int y, unsigned char* var, int maxlen);
int send_cmd(unsigned char req, unsigned char param);
void clearState();
void process(int bufsize, unsigned char* buffer);
void unblink();
void blink();
void term();
void main();

#endif
