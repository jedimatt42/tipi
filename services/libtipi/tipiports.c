
#include <Python.h>
#include <wiringPi.h>
#include <stdlib.h>
#include <stdio.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>


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

inline unsigned char readByte(int reg)
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

  return value;
}

static PyObject* 
tipi_getTD(PyObject *self, PyObject *args)
{
  unsigned char td_value = readByte(SEL_TD);

  return Py_BuildValue("i", td_value);
}

static PyObject* 
tipi_getTC(PyObject *self, PyObject *args)
{
  unsigned char tc_value = readByte(SEL_TC);

  return Py_BuildValue("i", tc_value);
}

inline void writeByte(unsigned char value, int reg) 
{
  int errors = 0;

  int ok = 0;

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
}

static PyObject* 
tipi_setRD(PyObject *self, PyObject *args)
{
  unsigned char rd_value;
  PyArg_ParseTuple(args, "b", &rd_value);

  writeByte(rd_value, SEL_RD);

  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject* 
tipi_setRC(PyObject *self, PyObject *args)
{
  unsigned char rc_value;
  PyArg_ParseTuple(args, "b", &rc_value);

  writeByte(rc_value, SEL_RC);

  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject* 
tipi_initGpio(PyObject *self, PyObject *args)
{
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

  Py_INCREF(Py_None);
  return Py_None;
}

static PyMethodDef TipiMethods[] = {
  {"getTD", tipi_getTD, METH_VARARGS, "get tipi input data"},
  {"getTC", tipi_getTC, METH_VARARGS, "set tipi input signals"},
  {"setRD", tipi_setRD, METH_VARARGS, "set tipi output data"},
  {"setRC", tipi_setRC, METH_VARARGS, "set tipi output signals"},
  {"initGpio", tipi_initGpio, METH_VARARGS, "set tipi gpio modes"},
  {NULL, NULL, 0, NULL}
};

static struct PyModuleDef moduledef = {
  PyModuleDef_HEAD_INIT,
  "tipiports",
  "Tipi GPIO register interface",
  -1,
  TipiMethods,
  NULL,
  NULL,
  NULL,
  NULL,
};

PyMODINIT_FUNC
PyInit_tipiports(void)
{
  PyObject *m;
  m = PyModule_Create(&moduledef);
  return m; /* if it fails, just return the NULL */
}

