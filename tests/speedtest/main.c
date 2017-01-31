
#include <vdp.h>
#include <system.h>

#define SCREEN_COLOR (COLOR_BLACK << 4) + COLOR_CYAN
#define ERROR_COLOR (COLOR_BLACK << 4) + COLOR_MEDRED
#define SUCCESS_COLOR (COLOR_BLACK << 4) + COLOR_LTGREEN

#define TI_DATA *((volatile unsigned char*)0x5fff) 
#define TI_CONTROL *((volatile unsigned char*)0x5ffd) 
#define RPI_DATA *((volatile unsigned char*)0x5ffb) 
#define RPI_CONTROL *((volatile unsigned char*)0x5ff9) 

#define ACK_MASK 0x03
#define SYN_BIT 0x02
#define RESET 0x01


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
  unsigned char next_syn = ((RPI_CONTROL + 1) & ACK_MASK) | SYN_BIT;
  TI_DATA = value;
  TI_CONTROL = next_syn;
  while ( (RPI_CONTROL & ACK_MASK) != next_syn ) {
    // wait until ack.
    debugInputs();
  }
}

unsigned char readByte(unsigned char* prev_rpi_syn) {
  unsigned char next_ack = 0;
  do {
    debugInputs();
    next_ack = RPI_CONTROL & ACK_MASK;
  } while ( *prev_rpi_syn == next_ack );
  unsigned char some_data = RPI_DATA;
  TI_CONTROL = next_ack;
  *prev_rpi_syn = next_ack;
  return some_data;
}

void main()
{
  int unblank = set_text();
  VDP_SET_REGISTER(VDP_REG_COL, SCREEN_COLOR);
  vdpmemset(0x0000,' ',nTextEnd);
  VDP_SET_REGISTER(VDP_REG_MODE1, unblank);
  charsetlc();

  writestring(1, 0, "TIPI Speedtest");

  writestring(3, 0, "start python speedtest.py...");

  unsigned char prev_rpi_syn = RESET;

  // Wait for RPI to reset control signals.
  TI_CONTROL = RESET;
  while( RPI_CONTROL != RESET ) {
    // be busy.
    debugInputs();
  }

  writestring(3, 0, "Testing.....................");

  unsigned int chksum = 0;
  for(int i = 0; i < 8192; i++) {
    chksum += readByte(&prev_rpi_syn);
  }
  writestring(4,4, "8k of data with check sum of:");
  writehex(5,8, chksum);

  // Wait for RPI to reset control signals.
  TI_CONTROL = RESET;
  while( RPI_CONTROL != RESET ) {
    // be busy.
    debugInputs();
  }

  chksum = 0;
  for(int i = 0; i < 8192; i++) {
    unsigned char value = i % 255;
    chksum += value;
    sendByte(value);
  }

  writestring(7,4, "8k of data sent with check sum of:");
  writehex(8,8, chksum);

  // Reset some state the vdp interrupt expects
  VDP_INT_CTRL=VDP_INT_CTRL_DISABLE_SPRITES|VDP_INT_CTRL_DISABLE_SOUND;
  VDP_SCREEN_TIMEOUT=1;
  halt();
}
