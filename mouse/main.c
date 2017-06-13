
#include <vdp.h>
#include <system.h>

#include "patterns.h"
#include "tipi.h"

#define SCREEN_COLOR (COLOR_BLACK << 4) + COLOR_CYAN

#define SPR_MOUSE0 0
#define SPR_MOUSE1 1
#define true 1
#define false 0

unsigned int pointerx;
unsigned int pointery;

void sprite_pos(unsigned int n, unsigned int r, unsigned int c) {
  unsigned int addr=gSprite+(n<<2);
  VDP_SET_ADDRESS_WRITE(addr);
  VDPWD=r;
  VDPWD=c;
}

void plotBit(unsigned int x, unsigned int y) {
  unsigned int addr = (8 * (x/8)) + (256 * (y/8)) + (y%8);
  VDP_SET_ADDRESS(addr);
  unsigned char bits = VDPRD;
  bits = bits | (0x80 >> (x%8));
  VDP_SET_ADDRESS_WRITE(addr);
  VDPWD = bits;
}

void main() {

  int unblank = set_bitmap(VDP_SPR_16x16);
  // VDP_SET_REGISTER(VDP_REG_COL, SCREEN_COLOR);
  vdpwriteinc(gImage,0,768);
  vdpmemset(gColor,SCREEN_COLOR,768*8);  
  vdpmemset(gPattern,0,768*8);

  // Load Sprite patterns
  vdpmemcpy(gSpritePat, gfx_point0, 32);
  vdpmemcpy(gSpritePat + 32, gfx_point1, 32);

  pointerx = 256/2;
  pointery = 192/2;

  sprite(SPR_MOUSE0, 0, COLOR_BLACK, pointery, pointerx);
  sprite(SPR_MOUSE1, 4, COLOR_WHITE, pointery, pointerx);

  VDP_SET_REGISTER(VDP_REG_MODE1, unblank);

  tipiEnable();
  tipiMouseOn();

  while(true) {
    VDP_WAIT_VBLANK_CRU

    tipiMouseRead();

    pointerx += (2 * mousex) / 3;
    pointery += (2 * mousey) / 3;

    if (pointerx > 0xF000) {
      pointerx = 0;
    } else if (pointerx > 255) {
      pointerx = 255;
    }

    if (pointery > 0xF000) {
      pointery = 0;
    } else if (pointery > 191) {
      pointery = 191;
    }

    sprite_pos(SPR_MOUSE0, pointery, pointerx);
    sprite_pos(SPR_MOUSE1, pointery, pointerx);

    if (mouseb & MB_LEFT) {
      plotBit(pointerx,pointery);
    }
    if (mouseb & MB_RIGHT) {
      vdpmemset(gPattern,0,768*8);
    }
  }

  tipiDisable();
}
