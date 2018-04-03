#include "ti_socket.h"
#include "tipi_msg.h"
#include <string.h>

#define TI_SOCKET_REQUEST 0x22
#define TI_SOCKET_OPEN 0x01
#define TI_SOCKET_CLOSE 0x02
#define TI_SOCKET_WRITE 0x03
#define TI_SOCKET_READ 0x04
#define socketId 0x00

unsigned char buffer[512];

unsigned char output[128];

unsigned char connect(unsigned char* hostname, unsigned char* port) {
  buffer[0] = TI_SOCKET_REQUEST;
  buffer[1] = socketId;
  buffer[2] = TI_SOCKET_OPEN;
  unsigned char* cursor = buffer + 3;
  strcpy(cursor, hostname);
  cursor += strlen(hostname);
  *cursor = ':';
  cursor++;
  strcpy(cursor, port);
  cursor += strlen(port);
  int bufsize = cursor - buffer;

  tipi_on();
  tipi_sendmsg(bufsize, buffer);
  bufsize = 0;
  tipi_recvmsg(&bufsize, buffer);
  tipi_off();

  return buffer[0];
}

// will send at most 122 byte character sequences (cause size of output buffer)
int send_chars(unsigned char* buf, int size) {
  output[0] = TI_SOCKET_REQUEST;
  output[1] = socketId;
  output[2] = TI_SOCKET_WRITE;

  if (size > 122) {
    size = 122;
  }
  for(int i=3; i<(3+size); i++) {
    output[i] = buf[i-3];
  }
  tipi_on();
  tipi_sendmsg(3 + size, output);
  int bufsize = 0;
  tipi_recvmsg(&bufsize, buffer);
  tipi_off();
  return buffer[0];
}

int read_socket() {
  output[0] = TI_SOCKET_REQUEST;
  output[1] = socketId;
  output[2] = TI_SOCKET_READ;
  output[3] = 2; // buffer size is 512 bytes
  output[4] = 0;
  tipi_on();
  tipi_sendmsg(5, output);
  int bufsize = 0;
  tipi_recvmsg(&bufsize, buffer);
  tipi_off();
  return bufsize;
}

