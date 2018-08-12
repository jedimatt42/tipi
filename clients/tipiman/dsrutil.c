#include "dsrutil.h"

#include <vdp.h>


unsigned char loadDir(const char* pathname, catHandler func) {
  struct PAB pab;
  
  unsigned char ferr = dsr_open(&pab, pathname, FBUF, DSR_TYPE_INPUT | DSR_TYPE_INTERNAL | DSR_TYPE_SEQUENTIAL, 38);
  if (ferr) {
    return ferr;
  }

  int recNo = 0;
  ferr = DSR_ERR_NONE;
  while(ferr == DSR_ERR_NONE) {
    unsigned char cbuf[38];
    ferr = dsr_read(&pab, recNo++);
    if (ferr == DSR_ERR_NONE) {
      // Now FBUF has the data... 
      vdpmemread(FBUF, cbuf, pab.CharCount);
      // process Record
      func(cbuf);
    }
  }

  ferr = dsr_close(&pab);
  if (ferr) {
    return ferr;
  }
}


//---- the following are meant to be easy, not fast ----

void initPab(struct PAB* pab) {
  pab->OpCode = DSR_OPEN;
  pab->Status = DSR_TYPE_DISPLAY | DSR_TYPE_VARIABLE | DSR_TYPE_SEQUENTIAL | DSR_TYPE_INPUT;
  pab->RecordLength = 80;
  pab->RecordNumber = 0;
  pab->ScreenOffset = 0;
  pab->NameLength = 0;
  pab->CharCount = 0;
}

unsigned char dsr_open(struct PAB* pab, const char* fname, int vdpbuffer, unsigned char flags, int reclen) {
  initPab(pab);
  pab->OpCode = DSR_OPEN;
  if (flags != 0) {
    pab->Status = flags;
  }
  if (reclen != 0) {
    pab->RecordLength = reclen;
  }
  pab->pName = (char*)fname;
  pab->VDPBuffer = vdpbuffer;

  return dsrlnk(pab, VPAB);
}

unsigned char dsr_close(struct PAB* pab) {
  pab->OpCode = DSR_CLOSE;

  return dsrlnk(pab, VPAB);
}

// the data read is in FBUF, the length read in pab->CharCount
// typically passing 0 in for record number will let the controller
// auto-increment it. 
unsigned char dsr_read(struct PAB* pab, int recordNumber) {
  pab->OpCode = DSR_READ;
  pab->RecordNumber = recordNumber;
  pab->CharCount = 0;

  unsigned char result = dsrlnk(pab, VPAB);
  vdpmemread(VPAB + 5, (&pab->CharCount), 1);
  return result;
}

