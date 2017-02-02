
#include <vdp.h>
#include <system.h>
#include <kscan.h>

#define SCREEN_COLOR (COLOR_BLACK << 4) + COLOR_CYAN

#define TI_DATA *((volatile unsigned char*)0x5fff) 
#define TI_CONTROL *((volatile unsigned char*)0x5ffd) 
#define RPI_DATA *((volatile unsigned char*)0x5ffb) 
#define RPI_CONTROL *((volatile unsigned char*)0x5ff9) 

#define ACK_MASK 0x03
#define SYN_BIT 0x02
#define RESET 0x01
#define DIR_REQUEST_BYTE 0x04

unsigned char prev_syn = RESET;

void writehex(unsigned int row, unsigned int col, const unsigned int value) {
  unsigned char buf[3] = { 0, 0, 0 };
  *((unsigned int*)buf) = byte2hex[value >> 8];
  writestring(row, col, buf);
  *((unsigned int*)buf) = byte2hex[0xFF & value];
  writestring(row, col + 2, buf);
}

void debugInputs() {
  writehex(0, 18, RPI_DATA);
  writehex(0, 24, RPI_CONTROL);
}

void sendByte(unsigned char value) {
  // read last ack to get counter and inc for next syn.
  prev_syn = ((prev_syn + 1) & ACK_MASK) | SYN_BIT;
  TI_DATA = value;
  TI_CONTROL = prev_syn;
  while ( (RPI_CONTROL & ACK_MASK) != prev_syn ) {
    // wait until ack.
    // debugInputs();
  }
}

unsigned char readByte() {
  unsigned char value = 0;
  prev_syn = (prev_syn + 1) & ACK_MASK | SYN_BIT | DIR_REQUEST_BYTE;
  TI_CONTROL = prev_syn;
  while( (RPI_CONTROL & ACK_MASK) != (prev_syn & ACK_MASK) ) {
    // debugInputs();
  }
  return RPI_DATA;
}

void resetProtocol() {
  // Wait for RPI to reset control signals.
  TI_CONTROL = RESET;
  while( RPI_CONTROL != RESET ) {
    // be busy.
    // debugInputs();
  }
}

void requestFile(unsigned char* filename) {
  unsigned char msg[] = "EA5.";
  for( int i = 0; i < 4; i++ ) {
    sendByte(msg[i]);
  }
  for( int i = 0; i < 20; i++ ) {
    sendByte(filename[i]);
  }
  sendByte(0x00);
}

void launch(int address) {
  int* code = (int*)0x8300;
  *code++ = 0x020C;   // li r12,>1000
  *code++ = 0x1000;   //
  *code++ = 0x1E00;   // sbz 0
  *code++ = 0x045B;   // b *r1
  __asm__("li r11,0\n\ta %0,r11\n\tb *%1" : : "r"(address), "r"(0x8300) );
}

void main()
{
  unsigned char filename[] = "AMBULANCE           ";
  int unblank = set_graphics(0);
  vdpmemset(0x0000,' ',nTextEnd);
  VDP_SET_REGISTER(VDP_REG_MODE1, unblank);
  charset();

  writestring(1, 0, "TIPI EA5 Loader");
  writestring(3, 0, "FILE: ");
  writestring(3, 6, filename );
  
  int idx = 3;
  unsigned char key = kscan(KSCAN_MODE_BASIC);
  while( 1 ) {
    if (KSCAN_STATUS == KSCAN_MASK && idx < 20) {
      if (key == 0x0D) {
        break;
      } else if (key == 0x08 && idx > 0) {
        idx--;
        *(filename + idx) = 0x20;
      } else {
        *(filename + idx++) = key;
      }
      writestring(3, 6, filename);
    }
    key = kscan(KSCAN_MODE_BASIC);
  }

  writestring(4, 0, "LOADING...");

  resetProtocol();

  // Send request to load file
  requestFile(filename);

  // No error checking :) 
  int ea5header = (((int) readByte()) << 8) + readByte();
  int size = (((int) readByte()) << 8) + readByte();
  int addr = (((int) readByte()) << 8) + readByte();
  // should be 0000
  writehex(0,10, ea5header);
  writehex(0,15, size);
  writehex(0,20, addr);

  // hack... all of my ea5 files are short 6 bytes...  so don't believe the size.
  unsigned char* copyaddr = (unsigned char*)addr;
  for( int i = 0; i < (size - 6); i++ ) {
    *copyaddr = readByte();
    copyaddr++;
    writehex(0,25, (int)copyaddr);
  }

  launch(addr);

  // Reset some state the vdp interrupt expects
  VDP_INT_CTRL=VDP_INT_CTRL_DISABLE_SPRITES|VDP_INT_CTRL_DISABLE_SOUND;
  VDP_SCREEN_TIMEOUT=1;
  halt();
}
