
#include <vdp.h>
#include <system.h>
#include <kscan.h>

#include "patterns.h"
#include "tipi.h"

#define SCREEN_COLOR (COLOR_BLACK << 4) + COLOR_CYAN

#define SPR_MOUSE0 0
#define SPR_MOUSE1 1
#define true 1
#define false 0

int pointerx;
int pointery;
int counter;

void sprite_pos(int n, int r, int c) {
  unsigned int adr=gSprite+(n<<2);
  VDP_SET_ADDRESS_WRITE(adr);
  VDPWD=r;
  VDPWD=c;
}

void main() {

  int unblank = set_graphics(VDP_SPR_16x16);
  VDP_SET_REGISTER(VDP_REG_COL, SCREEN_COLOR);
  vdpmemset(gImage,' ',nTextEnd);
  vdpmemset(gColor,SCREEN_COLOR,32);  
  VDP_SET_REGISTER(VDP_REG_MODE1, unblank);

  // Load Sprite patterns
  vdpmemcpy(gSpritePat, gfx_point0, 32);
  vdpmemcpy(gSpritePat + 32, gfx_point1, 32);

  counter = 0;
  pointerx = 256/2;
  pointery = 192/2;

  sprite(SPR_MOUSE0, 0, COLOR_BLACK, pointery, pointerx);
  sprite(SPR_MOUSE1, 4, COLOR_WHITE, pointery, pointerx);

  tipiEnable();
  tipiMouseOn();

  while(true) {
    VDP_WAIT_VBLANK_CRU
    counter++;

    tipiMouseRead();

    pointerx += mousex;
    pointery += mousey;

    sprite_pos(SPR_MOUSE0, pointery, pointerx);
    sprite_pos(SPR_MOUSE1, pointery, pointerx);
  }

  tipiMouseOff();
  tipiDisable();
}
