#ifndef _DSR_H
#define _DSR_H 1

#include <files.h>

#define VPAB 0x3000
#define FBUF 0x3200

#define DSR_STATUS_EOF DST_STATUS_EOF

struct __attribute__((__packed__)) DeviceServiceRoutine {
  char name[8];
  int crubase;
  int addr;
}; 

extern struct DeviceServiceRoutine dsrList[40];

struct __attribute__((__packed__)) DirEntry {
  char name[11];
  int type;
  int sectors;
  int reclen;
}; 

extern struct DirEntry lentries[200];
extern struct DirEntry rentries[200];

struct __attribute__((__packed__)) VolInfo {
  char name[11];
};

extern struct VolInfo lvol;
extern struct VolInfo rvol;

unsigned char dsr_open(struct PAB* pab, const char* fname, int vdpbuffer, unsigned char flags, int reclen);
unsigned char dsr_close(struct PAB* pab);
unsigned char dsr_read(struct PAB* pab, int recordNumber);
unsigned char dsr_write(struct PAB* pab, unsigned char* record);

unsigned char loadDir(const char* pathname, int leftOrRight);

#endif
