#ifndef _DSR_H
#define _DSR_H 1

#include <files.h>

#define VPAB 0x3000
#define FBUF 0x3200

#define DSR_STATUS_EOF DST_STATUS_EOF

unsigned char dsr_open(struct PAB* pab, const char* fname, int vdpbuffer, unsigned char flags, int reclen);
unsigned char dsr_close(struct PAB* pab);
unsigned char dsr_read(struct PAB* pab, int recordNumber);
unsigned char dsr_write(struct PAB* pab, unsigned char* record);

typedef int (*catHandler)(char* entry);

unsigned char loadDir(const char* pathname, catHandler func);

#endif
