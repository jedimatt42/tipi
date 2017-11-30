
#include <files.h>

#define DSR_STATUS_EOF DST_STATUS_EOF

#include <string.h>
#include <system.h>
#include <conio.h>

#define VPAB 0x3000
#define FBUF 0x3200

#define GPLWS ((unsigned int*)0x83E0)

#define PI_CONFIG "PI.CONFIG"
#define PI_STATUS "PI.STATUS"

unsigned char dsr_openDV(struct PAB* pab, char* fname, int vdpbuffer, unsigned char flags);
unsigned char dsr_close(struct PAB* pab);
unsigned char dsr_read(struct PAB* pab, int recordNumber);
unsigned char dsr_write(struct PAB* pab, unsigned char* record);

int strcmp(const char* a, const char* b);
int indexof(const char* str, char c);

void processStatusLine(char* cbuf);
void loadPiStatus();

void processConfigLine(char* cbuf);
void loadPiConfig();

void savePiConfig();

void getstr(int x, int y, char* var);

char ipaddress[79]; // generically k=v values from files would be at most 78 characters. 
char version[79];
int crubase;

char dsk1_dir[79];
char dsk2_dir[79];
char dsk3_dir[79];
char wifi_ssid[79];
char wifi_psk[79];

int wifi_dirty;
int disks_dirty;

void waitForDebugger(const char* msg) {
  int x = 0;
  gotoxy(20,23); cprintf("wfd! %s", msg);
  while (x == 0) {
  }
}

void showCrubase(int crubase) {
  gotoxy(0,1);
  cprintf("CRUBASE: %x", crubase);
}

void showValue(int x, int y, const char* val) {
  gotoxy(x,y);
  cclear(40 - x);
  gotoxy(x,y);
  cputs(val);
}

void initGlobals() {
  strcpy(ipaddress,"");
  strcpy(version,"");
  strcpy(dsk1_dir,"");
  strcpy(dsk2_dir,"");
  strcpy(dsk3_dir,"");
  strcpy(wifi_ssid,"");
  strcpy(wifi_psk,"");
  crubase = 0;

  wifi_dirty = 0;
  disks_dirty = 0;
}

void setupScreen() {
  set_text();
  charset();
  bgcolor(COLOR_CYAN);
  textcolor(COLOR_BLACK);
}

void layoutScreen() {
  clrscr();
  gotoxy(0,0);
  cputs("TIPI Config");
  showCrubase(crubase);

  gotoxy(16,0);
  cputs("Version: ");
  gotoxy(16,1);
  cputs("     IP: ");
  gotoxy(0,2);
  chline(40);
  gotoxy(0,4);
  chline(40);

  gotoxy(0,5);
  cputs("Drive Mappings");
  gotoxy(2,6);
  cputs("1) DSK1=");
  gotoxy(2,7);
  cputs("2) DSK2=");
  gotoxy(2,8);
  cputs("3) DSK3=");

  gotoxy(0,9);
  chline(40);
  gotoxy(0,10);
  cputs("WiFi Settings");
  gotoxy(2,11);
  cputs("S) SSID=");
  gotoxy(2,12);
  cputs("P)  PSK=");
  gotoxy(0,13);
  chline(40);

  gotoxy(0,22);
  chline(40);
  gotoxy(6,23);
  cputs("Q) quit, W) write, R) reload");
}

void main()
{
  initGlobals();
  setupScreen();

  layoutScreen();


  loadPiStatus();
  loadPiConfig();

  unsigned char key = 0;
  do {
    gotoxy(23,35);
    
    while(!kbhit()) {}

    key = cgetc();
    switch(key) {
      case '1':
        disks_dirty = 1;
        getstr(10,6,dsk1_dir);
        showValue(10,6,dsk1_dir);
        break;
      case '2':
        disks_dirty = 1;
        getstr(10,7,dsk2_dir);
        showValue(10,7,dsk2_dir);
        break;
      case '3':
        disks_dirty = 1;
        getstr(10,8,dsk3_dir);
        showValue(10,8,dsk3_dir);
        break;
      case 'S':
        wifi_dirty = 1;
        getstr(10,11,wifi_ssid);
        showValue(10,11,wifi_ssid);
        break;
      case 'P':
        wifi_dirty = 1;
        getstr(10,12,wifi_psk);
        showValue(10,12,wifi_psk);
        break;
      case 'R':
        disks_dirty = 0;
        wifi_dirty = 0;
        loadPiStatus();
        loadPiConfig();
        break;
      case 'W':
        savePiConfig();
        disks_dirty = 0;
        wifi_dirty = 0;
        break;
    }


  } while(key != 'Q');

  gotoxy(0,3);
  cputs("quiting...");
  __asm__("clr r0\n\tblwp *r0");
}

void loadPiStatus() {
  struct PAB pab;

  gotoxy(0,3);
  cputs("Loading PI.STATUS");
  
  unsigned char ferr = dsr_openDV(&pab, PI_STATUS, FBUF, DSR_TYPE_INPUT);
  if (ferr) {
    cprintf(" ERROR: %x", ferr);
    halt();
  }

  // see if we can steal the crubase
  // should work immediately after a dsrlnk if interrupts are off.
  crubase = GPLWS[12];
  showCrubase(crubase);

  int recNo = 0;
  ferr = DSR_ERR_NONE;
  while(ferr == DSR_ERR_NONE) {
    unsigned char cbuf[81];
    ferr = dsr_read(&pab, 0);
    gotoxy(0,22);
    if (ferr == DSR_ERR_NONE) {
      // Now FBUF has the data... 
      vdpmemread(FBUF, cbuf, pab.CharCount);
      cbuf[pab.CharCount] = 0;
      processStatusLine(cbuf);
    }
  }

  showValue(25, 0, version);
  showValue(25, 1, ipaddress);

  ferr = dsr_close(&pab);
  if (ferr) {
    cprintf("Close ERROR: %x", ferr);
    halt();
  }
  gotoxy(0,3);
  cclear(40);
}

void processStatusLine(char* cbuf) {
  int i = indexof(cbuf, '=');
  if (i == -1) {
    return;
  }
  cbuf[i] = 0;
  char* val = cbuf + i + 1;
  if (0 == strcmp(cbuf, "VERSION")) {
    strcpy(version, val);
  } else if (0 == strcmp(cbuf, "IP_WLAN0")) {
    strcpy(ipaddress, val);
  } else if (0 == strcmp(cbuf, "IP_ETH0")) {
    strcpy(ipaddress, val);
  }
}

void loadPiConfig() {
  struct PAB pab;

  gotoxy(0,3);
  cputs("Loading PI.CONFIG");
  
  unsigned char ferr = dsr_openDV(&pab, PI_CONFIG, FBUF, DSR_TYPE_INPUT);
  if (ferr) {
    cprintf(" ERROR: %x", ferr);
    halt();
  }

  int recNo = 0;
  ferr = DSR_ERR_NONE;
  while(ferr == DSR_ERR_NONE) {
    unsigned char cbuf[81];
    ferr = dsr_read(&pab, 0);
    gotoxy(0,22);
    if (ferr == DSR_ERR_NONE) {
      // Now FBUF has the data... 
      vdpmemread(FBUF, cbuf, pab.CharCount);
      cbuf[pab.CharCount] = 0;
      processConfigLine(cbuf);
    }
  }

  showValue(10, 6, dsk1_dir);
  showValue(10, 7, dsk2_dir);
  showValue(10, 8, dsk3_dir);
  showValue(10, 11, wifi_ssid);
  showValue(10, 12, wifi_psk);

  ferr = dsr_close(&pab);
  if (ferr) {
    cprintf("Close ERROR: %x", ferr);
    halt();
  }
  gotoxy(0,3);
  cclear(40);
}

void processConfigLine(char* cbuf) {
  int i = indexof(cbuf, '=');
  if (i == -1) {
    return;
  }
  cbuf[i] = 0;
  char* val = cbuf + i + 1;
  if (0 == strcmp(cbuf, "DSK1_DIR")) {
    strcpy(dsk1_dir, val);
  } else if (0 == strcmp(cbuf, "DSK2_DIR")) {
    strcpy(dsk2_dir, val);
  } else if (0 == strcmp(cbuf, "DSK3_DIR")) {
    strcpy(dsk3_dir, val);
  } else if (0 == strcmp(cbuf, "WIFI_SSID")) {
    strcpy(wifi_ssid, val);
  } else if (0 == strcmp(cbuf, "WIFI_PSK")) {
    strcpy(wifi_psk, val);
  }
}

void getstr(int x, int y, char* var) {
  gotoxy(x,y);
  cclear(30);
  gotoxy(x,y);
  for(int i=0; i<79; i++) {
    var[i] = 0;
  }
  unsigned char key = 0;
  int idx = 0;
  while(key != 13) {
    key = cgetc();
    switch(key) {
      case 13:
        break;
      case 8:
        if (idx > 0) {
          var[--idx] = 0;
          gotoxy(x+idx,y);
          cputc(' ');
          gotoxy(x+idx,y);
        }
        break;
      default:
        if (key >= 32 && key <= 122) {
          var[idx++] = key;
          cputc(key);
        }
    }
  }
  var[idx] = 0;
}

void savePiConfig() {
  if (disks_dirty == 0 && wifi_dirty == 0) {
    gotoxy(0,3);
    cputs("No changes");
    return;
  }

  struct PAB pab;

  gotoxy(0,3);
  cputs("Saving PI.CONFIG");
  
  unsigned char ferr = dsr_openDV(&pab, PI_CONFIG, FBUF, DSR_TYPE_APPEND);
  if (ferr) {
    cprintf(" ERROR: %x", ferr);
    halt();
  }

  unsigned char line[81];

  if (disks_dirty) {
    strcpy(line, "DSK1_DIR=");
    strcpy(line+9, dsk1_dir);
    ferr = dsr_write(&pab, line);
    if (ferr) {
      cprintf(" ERROR: %x", ferr);
      halt();
    }
    strcpy(line, "DSK2_DIR=");
    strcpy(line+9, dsk2_dir);
    ferr = dsr_write(&pab, line);
    if (ferr) {
      cprintf(" ERROR: %x", ferr);
      halt();
    }
    strcpy(line, "DSK3_DIR=");
    strcpy(line+9, dsk3_dir);
    ferr = dsr_write(&pab, line);
    if (ferr) {
      cprintf(" ERROR: %x", ferr);
      halt();
    }
  }

  if (wifi_dirty) {
    strcpy(line, "WIFI_SSID=");
    strcpy(line+10, wifi_ssid);
    ferr = dsr_write(&pab, line);
    if (ferr) {
      cprintf(" ERROR: %x", ferr);
      halt();
    }
    strcpy(line, "WIFI_PSK=");
    strcpy(line+9, wifi_psk);
    ferr = dsr_write(&pab, line);
    if (ferr) {
      cprintf(" ERROR: %x", ferr);
      halt();
    }
  }

  ferr = dsr_close(&pab);
  if (ferr) {
    cprintf("Close ERROR: %x", ferr);
    halt();
  }
  gotoxy(0,3);
  cclear(40);
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

// Configures a PAB for filename and DV80, and opens the file
unsigned char dsr_openDV(struct PAB* pab, char* fname, int vdpbuffer, unsigned char flags) {
  initPab(pab);
  pab->OpCode = DSR_OPEN;
  pab->Status = DSR_TYPE_DISPLAY | DSR_TYPE_VARIABLE | DSR_TYPE_SEQUENTIAL | flags;
  pab->RecordLength = 80;
  pab->pName = fname;
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

unsigned char dsr_write(struct PAB* pab, unsigned char* record) {
  pab->OpCode = DSR_WRITE;
  int len = strlen(record);
  vdpmemcpy(pab->VDPBuffer, record, len);
  pab->CharCount = len;

  return dsrlnk(pab, VPAB);
}

// utilities

int strcmp(const char* a, const char* b) {
  int i=0;
  do {
    if (a[i] == '\0') {
      return a[i] - b[i];
    }
    i++;
  } while(a[i] == b[i]);
  return a[i] - b[i];
}

int indexof(const char* str, char c) {
  int i=0;
  while(str[i] != 0) {
    if (str[i] == c) {
      return i;
    }
    i++;
  }
  return -1;
}
