#include "tifloat.h"
 
int ti_floatToInt(unsigned char* bytes) {
  if (bytes[0] == 8) {
    int word0 = (bytes[1] << 8) + bytes[2];
    int word1 = bytes[3];
        int val = 0;
    int neg = 1;
    char hb = (word0 >> 8) & 0xff;

    if ((word0 & 0xb000) == 0xb000) {
      neg = -1;
      word0 = ~(word0 - 1);
      hb = (word0 >> 8) & 0xff;
    }

    if (hb == 0x40) {
      val = word0 & 0xff;
    } else if (hb == 0x41) {
      val = ((word0 & 0x00ff) * 100) + (word1 & 0x00ff);
    } else {
      val = 0;
    }

    if (neg == -1) {
      val = -1 * val;
    }
    return val;
  } else {
    return 0;
  }
}
