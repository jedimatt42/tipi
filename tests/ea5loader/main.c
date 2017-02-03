
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
  unsigned char buf[] = { 0, 0, 0 };
  *((unsigned int*)buf) = byte2hex[value >> 8];
  buf[2] = 0;
  writestring(row, col, buf);
  *((unsigned int*)buf) = byte2hex[0xFF & value];
  buf[2] = 0;
  writestring(row, col + 2, buf);
}

void sendByte(unsigned char value) {
  // read last ack to get counter and inc for next syn.
  prev_syn = ((prev_syn + 1) & ACK_MASK) | SYN_BIT;
  TI_DATA = value;
  TI_CONTROL = prev_syn;
  while ( (RPI_CONTROL & ACK_MASK) != prev_syn ) {
    // wait until ack.
  }
}

unsigned char readByte() {
  unsigned char value = 0;
  prev_syn = (prev_syn + 1) & ACK_MASK | SYN_BIT | DIR_REQUEST_BYTE;
  TI_CONTROL = prev_syn;
  while( (RPI_CONTROL & ACK_MASK) != (prev_syn & ACK_MASK) ) {
  }
  return RPI_DATA;
}

unsigned int readWord() {
  return (((unsigned int) readByte()) << 8) + readByte();
}

void resetProtocol() {
  // Wait for RPI to reset control signals.
  TI_CONTROL = RESET;
  while( RPI_CONTROL != RESET ) {
    // be busy.
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
  __asm__("b *%0" : : "r"(address) );
}

void main()
{
  int filename_size = 20;
  unsigned char filename[] = "                    ";
  int unblank = set_graphics(0);
  vdpmemset(0x0000,' ',nTextEnd);
  VDP_SET_REGISTER(VDP_REG_MODE1, unblank);
  charset();

  writestring(1, 0, "TIPI EA5 Loader");
  writestring(3, 0, "FILE: ");
  writestring(3, 6, filename );
  
  int idx = 0;
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

  int name_end = 19;
  while( filename[name_end] == 0x20 ) {
    name_end--;
  }

  writestring(4, 0, "LOADING...");

  unsigned int launchAddr = 0x0000;
  unsigned int ea5header = 0xFFFF;

  while ( ea5header == 0xFFFF ) {
    resetProtocol();
    writestring(3, 6, filename);

    // Send request to load file
    requestFile(filename);

    // No error checking :)
    ea5header = readWord();
    unsigned int size = readWord();
    unsigned int addr = readWord();

    writehex(0,10, ea5header);
    writehex(0,15, size);
    writehex(0,20, addr);

    // size is file size, not data size. so filesize - 6 bytes of header == data size.
    size -= 6;

    // stash addr away the first time.
    if (launchAddr == 0x0000) {
      launchAddr = addr;
    }

    unsigned char* copyaddr = (unsigned char*)addr;
    for( int i = 0; i < size; i++ ) {
      *copyaddr++ = readByte();
    }

    // increment file name to load next segment if necessary.
    filename[name_end]++;
  }

  launch(launchAddr);
}
