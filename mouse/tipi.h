
#define CRU 0x1000
#define TC *((volatile unsigned char*)0x5FFD)
#define TD *((volatile unsigned char*)0x5FFF)
#define RC *((volatile unsigned char*)0x5FF9)
#define RD *((volatile unsigned char*)0x5FFB)

#define TSRSET 0x01
#define TSWB 0x02
#define TSRB 0x06
#define TSACKM 0x03

void tipiEnable() {
  __asm__("li r12,>1000\n\tsbo 0");
}


void tipiDisable() {
  __asm__("li r12,>1000\n\tsbz 0");
}

void tipi_Reset() {
  TC = TSRSET;
  while(RC != TSRSET) { /* wait. */  }
}

char mousex;
char mousey;
char mouseb;

void tipiMouseOn() {
  mousex = 0;
  mousey = 0;
  mouseb = 0;
}

void tipiMouseOff() {

}

void tipiMouseRead() {
  tipi_Reset();
  TD = 0x00;
  TC = TSWB;
  while(RC != TSWB) { /* wait */ }
  TD = 0x01;
  TC = TSWB + 1;
  while(RC != TSWB + 1) { /* wait */ }
  TD = 0x20;
  TC = TSWB;
  while(RC != TSWB) { /* wait */ }

  // read response
  tipi_Reset();
  TC = TSRB;
  while(RC != TSWB) { /* wait */ }
  mousex = RD; 
  TC = TSRB + 1;
  while(RC != (TSWB + 1)) { /* wait */ }
  mousey = RD;
  TC = TSRB;
  while(RC != TSWB) { /* wait */ }
  mouseb = RD;
}

