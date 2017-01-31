
#include <vdp.h>
#include <system.h>

#define SCREEN_COLOR (COLOR_BLACK << 4) + COLOR_CYAN
#define ERROR_COLOR (COLOR_BLACK << 4) + COLOR_MEDRED
#define SUCCESS_COLOR (COLOR_BLACK << 4) + COLOR_LTGREEN

unsigned char* ti_data = (char*) 0x5fff;
unsigned char* ti_control = (char*) 0x5ffd;
volatile unsigned char* rpi_data = (char*) 0x5ffb;
volatile unsigned char* rpi_control = (char*) 0x5ff9;

#define ACK_MASK 0x03
#define SYN_BIT 0x02


void writehex(unsigned int row, unsigned int col, const unsigned int value) {
  unsigned char buf[3] = { 0, 0, 0 };
  *((unsigned int*)buf) = byte2hex[value >> 8];
  writestring(row, col, buf);
  *((unsigned int*)buf) = byte2hex[0xFF & value];
  writestring(row, col + 2, buf);
}

void sendByte(unsigned char value) {
  // read last ack to get counter and inc for next syn.
  unsigned char next_syn = ((*rpi_control + 1) & ACK_MASK) | SYN_BIT;
  *ti_data = value;
  *ti_control = next_syn;
  while ( (*rpi_control & ACK_MASK) != next_syn ) {
    // wait until ack.
  }
}

char readByte(char* prev_rpi_syn) {
  char next_ack = 0;
  do {
    next_ack = *rpi_control & ACK_MASK;
  } while ( *prev_rpi_syn == next_ack );
  char some_data = *rpi_data;
  *ti_control = next_ack;
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

  char prev_rpi_syn = 0;

  writestring(3, 0, "start python speedtest.py...");

  unsigned int chksum = 0;
  for(int i = 0; i < 8192; i++) {
    chksum += (unsigned char) readByte(&prev_rpi_syn);
  }
  writestring(4,4, "8k of data with check sum of:");
  writehex(5,8, chksum);

  chksum = 0;
  for(int i = 0; i < 8192; i++) {
    char value = i % 255;
    chksum += (unsigned char) value;
    sendByte(value);
  }

  writestring(7,4, "8k of data sent with check sum of:");
  writehex(8,8, chksum);

  // Reset some state the vdp interrupt expects
  VDP_INT_CTRL=VDP_INT_CTRL_DISABLE_SPRITES|VDP_INT_CTRL_DISABLE_SOUND;
  VDP_SCREEN_TIMEOUT=1;
  halt();
}
