
#include <Python.h>
#include <wiringPi.h>
#include <stdlib.h>
#include <stdio.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <stdarg.h>

// Serial output for RD & RC (BCM pin numbers)
#define PIN_R_RT 13
#define PIN_R_CD 21
#define PIN_R_CLK 6
#define PIN_R_DOUT 16
#define PIN_R_DIN 20
#define PIN_R_LE 19

#define SEL_RC 0
#define SEL_RD 1
#define SEL_TC 2
#define SEL_TD 3

// volatile to force slow memory access.
volatile long delmem = 55;

int delayloop = 50;

//#define LOG
#ifdef LOG
static const char *reg_names[] = {"RC","RD","TC","TD"};
static void log_printf(const char *fmt, ...)
{
  static FILE *log = NULL;
  if (!log) {
    log = fopen("/var/log/tipi/tipiports.log", "w");
    fprintf(log, "log opened\n");
  }

  va_list ap;
  va_start(ap, fmt);
  vfprintf(log, fmt, ap);
  va_end(ap);
  fflush(log);
}
#else
#define log_printf(...) do{}while(0)
#endif


char* errorsFifo = "/tmp/tipierrors";

inline void signalDelay(void)
{
  // delayMicroseconds(1L);
  int i = 0;
  for(i = 0; i < delayloop; i++) {
    delmem *= i;
  }
}

inline void setSelect(int reg)
{
  digitalWrite(PIN_R_RT, reg & 0x02);
  digitalWrite(PIN_R_CD, reg & 0x01);
  signalDelay();
}

inline unsigned char parity(unsigned char input) {
    unsigned char piParity = input;
    piParity ^= piParity >> 4;
    piParity ^= piParity >> 2;
    piParity ^= piParity >> 1;
    return piParity & 0x01;
}

void writeErrors(int errors) {
  int fd = open(errorsFifo, O_WRONLY);
  write(fd, (void*)&errors, 2);
  close(fd);
}


static unsigned char readReg(int reg)
{
  unsigned char value = 0;

  int errors = 0;

  int ok = 0;
  while(! ok) {
    value = 0;

    setSelect(reg);
    signalDelay();

    digitalWrite(PIN_R_LE, 1);
    signalDelay();
    digitalWrite(PIN_R_CLK, 1);
    signalDelay();
    digitalWrite(PIN_R_CLK, 0);
    signalDelay();
    digitalWrite(PIN_R_LE, 0);
    signalDelay();

    int i;
    for (i=7; i>=0; i--) {
      digitalWrite(PIN_R_CLK, 1);
      signalDelay();
      digitalWrite(PIN_R_CLK, 0);
      signalDelay();
      value |= digitalRead(PIN_R_DIN) << i;
    }

    // read the parity bit
    digitalWrite(PIN_R_CLK, 1);
    signalDelay();
    digitalWrite(PIN_R_CLK, 0);
    signalDelay();
    unsigned char tipiParity = digitalRead(PIN_R_DIN);

    unsigned char piParity = parity(value);

    ok = piParity == tipiParity;
    if (!ok) {
      errors++;
    }
  }
  {
    static unsigned char last[4] = {};
    if (last[reg] != value)
      log_printf("%s=>%02x\n", reg_names[reg], value);
    last[reg] = value;
  }
  return value;
}

static void writeReg(unsigned char value, int reg)
{
  int errors = 0;

  int ok = 0;
  log_printf("%s<=%02x\n", reg_names[reg], value);

  while (!ok) {
    setSelect(reg);

    int i;
    for (i=7; i>=0; i--) {
      digitalWrite(PIN_R_DOUT, (value >> i) & 0x01);
      signalDelay();
      digitalWrite(PIN_R_CLK, 1);
      signalDelay();
      digitalWrite(PIN_R_CLK, 0);
      signalDelay();
    }

    // read the parity bit
    signalDelay();
    unsigned char tipiParity = digitalRead(PIN_R_DIN);

    unsigned char piParity = parity(value);

    ok = piParity == tipiParity;
    if (!ok) {
      errors++;
    }
  }

  digitalWrite(PIN_R_LE, 1);
  signalDelay();
  digitalWrite(PIN_R_CLK, 1);
  signalDelay();
  digitalWrite(PIN_R_CLK, 0);
  signalDelay();
  digitalWrite(PIN_R_LE, 0);
  signalDelay();

  if (errors != 0) {
    writeErrors(errors);
  }
}





#define RESET 0xf1
#define TSWB  0x02
#define TSRB  0x06

#define BACKOFF_DELAY 10000

/*
# Low Level
# ---------
#
# Control bits in TC or RC are used to indicate the status of the data byte.
#
# All communication is driven from the TI. The PI polls the TC (TI Control)
# register to see wait for it to indicate the expected state. This is always
# in lock-step. If waiting for a byte receive request, the PI will do nothing
# other than wait for a that request. If trying send a byte, it will wait
# until the TI indicates that it wants a byte.
#
# A total value of 0x00 is never used for control registers as that is the
# powerup state.
#
# Data transmission, sending strings of bytes, the TC and RC registers are
# used to send something like syn - ack bytes.
# ( bit ordering 0 is LSB )
#
# * bit 0 is a single bit rolling counter.
# * bit 1 indicates the TI is writing a byte
# * bit 2 indicates the TI is requesting a byte
#
# Data registers are always set first, and then control registers are set
# to indicate that this data is ready for the purpose indicated.
#
# RC should always equal TC
# The next expected TC toggles bit 0, and the PI waits until it sees that
# request.
#
# Messaging
# ---------
#
# A byte string message is always prefixed by a word ( 16 bits ) of length,
# then the sequence of bytes. If the TI is sending, then the PI receives
# until gets all the bytes described by the length. As is true for the
# inverse direction. The 'reset' handshake is performed at the beginning
# of each message send. Then the message bytes are sent as:
#
# * msb(len)
# * lsb(len)
# * message
#
*/

static unsigned char prev_syn = 0;

/*
 * Block until both sides show control bits reset
 * The TI resets first, and then RPi responds
 * Returns -1 if BACKOFF timeout expires
 *
 * TC -> 0xF1, RC -> 0xF1
 */
static int resetProtocol(void)
{
  // And wait for the TI to signal RESET
  int bail = 0;
  int backoff = BACKOFF_DELAY;
  prev_syn = 0;
  log_printf("RESET waiting\n");
  while (prev_syn != RESET) {
    backoff--;
    if (backoff < 1) {
      struct timespec ts10ms = {0/*s*/, 10000000/*ns*/};
      backoff = 1;
      nanosleep(&ts10ms, NULL);
      bail++;
      if (bail > 50) {
        log_printf("RESET bail\n");
        PyErr_SetString(PyExc_ValueError, "safepoint");
        return -1; /* raise BackOffException('safepoint') */
      }
    }
    prev_syn = readReg(SEL_TC);
  }
  // Reset the control signals
  log_printf("RESET ack\n");
  writeReg(RESET, SEL_RC);
  return 0;
}

// change mode to sending bytes
static void modeSend(void)
{
  // actual send calls will always pre-increment this, so we start a
  // series by making sure the low bit will increment to zero.
  prev_syn = TSRB + 1;
}

// transmit a byte when TI requests it
static void sendByte(unsigned char byte)
{
  unsigned char next_syn = ((prev_syn + 1) & 0x01) | TSRB;
  while (prev_syn != next_syn)
    prev_syn = readReg(SEL_TC);
  writeReg(byte, SEL_RD);
  writeReg(prev_syn, SEL_RC);
}

// change mode to sending bytes
static void modeRead(void)
{
  // actual send calls will always pre-increment this, so we start a
  // series by making sure the low bit will increment to zero.
  prev_syn = TSWB + 1;
}

static unsigned char readByte(void)
{
  unsigned char next_syn = ((prev_syn + 1) & 0x01) | TSWB;
  while (prev_syn != next_syn)
    prev_syn = readReg(SEL_TC);
  unsigned char val = readReg(SEL_TD);
  writeReg(prev_syn, SEL_RC);
  return val;
}


static PyObject* gpio_readMsg(void)
{
  if (resetProtocol() < 0)
    return NULL;
  modeRead();
  int msglen = readByte() << 8;
  msglen |= readByte();

  PyObject *message = PyByteArray_FromStringAndSize("", 0);
  PyByteArray_Resize(message, msglen);
  Py_buffer buffer;
  if (PyObject_GetBuffer(message, &buffer, PyBUF_CONTIG) >= 0) {
    int i;
    unsigned char *buf = buffer.buf;
    for (i = 0; i < msglen; i++)
      buf[i] = readByte();
  }
  return message;
}

static PyObject* gpio_sendMsg(unsigned char *data, int len)
{
  if (resetProtocol() < 0)
    return NULL;
  modeSend();
  sendByte(len >> 8);
  sendByte(len & 0xff);

  int i;
  for (i = 0; i < len; i++)
    sendByte(data[i]);

  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject* gpio_sendMouseEvent(void)
{
  static char buttons = 0;
  static int fd = -1;
  char buf[4] = {buttons, 0, 0};

  if (fd == -1) {
    fd = open("/dev/input/mice", O_RDONLY | O_NONBLOCK);
    if (fd == -1) {
      Py_INCREF(Py_None);
      return Py_None;
    }
  }
  if (read(fd, buf, 3) == 3) {
    buttons = buf[0];
    buf[2] = -buf[2];
  }
  buf[3] = buttons;
  // send [dx, -dy, buttons]
  return gpio_sendMsg((unsigned char*)(buf+1), 3);
}



static PyObject* (*readMsg)(void) = gpio_readMsg;
static PyObject* (*sendMsg)(unsigned char *, int) = gpio_sendMsg;
static PyObject* (*sendMouseEvent)(void) = gpio_sendMouseEvent;


static PyObject*
tipi_sendMsg(PyObject *self, PyObject *args)
{
  PyObject *arg1, *result;
  if (!PyArg_ParseTuple(args, "O", &arg1))
    return NULL;

  if (PyList_Check(arg1)) {
    int len = PyList_Size(arg1);
    unsigned char *buf = alloca(len);
    int i;
    for (i = 0; i < len; i++) {
      PyObject *op = PyList_GET_ITEM(arg1, i);
      buf[i] = PyLong_AsLong(op);
    }
    result = sendMsg(buf, len);

  } else {
    Py_buffer buffer;
    if (PyObject_GetBuffer(arg1, &buffer, PyBUF_CONTIG_RO) < 0)
      return NULL;
    result = sendMsg(buffer.buf, buffer.len);
    PyBuffer_Release(&buffer);
  }
  return result;
}

static PyObject*
tipi_readMsg(PyObject *self, PyObject *args)
{
  return readMsg();
}

static PyObject*
tipi_sendMouseEvent(PyObject *self, PyObject *args)
{
  return sendMouseEvent();
}



static PyObject*
tipi_initGpio(PyObject *self, PyObject *args)
{
  // determine websocket mode and web path from env
  const char* tipiWebSock = getenv("TIPI_WEBSOCK");
  if (tipiWebSock != NULL) {
    // functions from websock.c
    extern void websocket_init(const char *path_to_web_root);
    extern PyObject* websocket_readMsg(void);
    extern PyObject* websocket_sendMsg(unsigned char *, int);
    extern PyObject* websocket_sendMouseEvent(void);

    websocket_init(tipiWebSock);
    readMsg = websocket_readMsg;
    sendMsg = websocket_sendMsg;
    sendMouseEvent = websocket_sendMouseEvent;

    log_printf("websocket mode\n");

  } else {
    log_printf("gpio mode\n");

    // get signalling delay from env
    const char* tipiSigEnv = getenv("TIPI_SIG_DELAY");
    if (tipiSigEnv==NULL) {
      delayloop = 0;
    } else {
      delayloop = atoi(tipiSigEnv);
    }

    wiringPiSetupGpio();

    pinMode(PIN_R_RT, OUTPUT);
    pinMode(PIN_R_CD, OUTPUT);
    pinMode(PIN_R_CLK, OUTPUT);
    pinMode(PIN_R_DOUT, OUTPUT);
    pinMode(PIN_R_LE, OUTPUT);
    pinMode(PIN_R_DIN, INPUT);
    // This line is driven from CPLD directly
    // enable the pull up on the input pin
    // to enhance CPLD ability to signal HIGH
    pullUpDnControl(PIN_R_DIN, PUD_UP);

    digitalWrite(PIN_R_RT, 0);
    digitalWrite(PIN_R_CD, 0);
    digitalWrite(PIN_R_CLK, 0);
    digitalWrite(PIN_R_DOUT, 0);
    digitalWrite(PIN_R_LE, 0);
  }

  Py_INCREF(Py_None);
  return Py_None;
}

static PyMethodDef TipiMethods[] = {
  {"initGpio", tipi_initGpio, METH_VARARGS, "set tipi gpio modes"},
  {"sendMsg", tipi_sendMsg, METH_VARARGS, "send tipi message"},
  {"readMsg", tipi_readMsg, METH_VARARGS, "read tipi message"},
  {"sendMouseEvent", tipi_sendMouseEvent, METH_VARARGS, "send mouse event"},
  {NULL, NULL, 0, NULL}
};

static struct PyModuleDef TipiModule = {
  PyModuleDef_HEAD_INIT,
  "tipiports",
  NULL, /* module documentation */
  -1,  /* global variable state */
  TipiMethods
};

PyMODINIT_FUNC
PyInit_tipiports(void)
{
  return PyModule_Create(&TipiModule);
}
