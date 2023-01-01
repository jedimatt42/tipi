
#include <Python.h>

#include <stdlib.h>
#include <stdio.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <stdarg.h>

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

#define SEL_RC 0
#define SEL_RD 1
#define SEL_TC 2
#define SEL_TD 3

static int* tipi_control_file;
static int* tipi_data_file;

static void writeReg(unsigned char value, int reg)
{
  // The PI can write to RC and RD only.
  int* file;
  if (reg == SEL_RC) {
    file = tipi_control_file;
  } else if (reg == SEL_RD) {
    file = tipi_data_file;
  }
  write(file, &value, 1);
}

static unsigned char readReg(int reg)
{
  unsigned char value;
  // The PI can read from only TC and TD.
  int* file;
  if (reg == SEL_TC) {
    file = tipi_control_file;
  } else if (reg == SEL_TD) {
    file = tipi_data_file;
  }
  read(file, &value, 1);
  return value;
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
      backoff = 1;
      usleep(10000/*us*/); // 10ms
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
  log_printf("gpio kernel driver mode\n");

  tipi_control_file = open("/dev/tipi_control", O_RDWR);
  tipi_data_file = open("/dev/tipi_data", O_RDWR);

  if (tipi_control_file == -1) {
    log_printf("could not open /dev/tipi_control\n");
  }
  if (tipi_data_file == -1) {
    log_printf("could not open /dev/tipi_data\n");
  }

  // need to set RC and RD to 0 so 4A knows 
  // pi is back online during certain events
  writeReg(0, SEL_RD);
  writeReg(0, SEL_RC);

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
  "tipiports_chardev",
  NULL, /* module documentation */
  -1,  /* global variable state */
  TipiMethods,
  NULL,
  NULL,
  NULL,
  NULL
};

PyMODINIT_FUNC
PyInit_tipiports_chardev(void)
{
  return PyModule_Create(&TipiModule);
}
