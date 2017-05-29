
#include <Python.h>
#include <wiringPi.h>

// Serial output for RD & RC (BCM pin numbers)
#define PIN_REG0 26
#define PIN_REG1 19
#define PIN_SHCLK 4
#define PIN_SDATA_OUT 13
#define PIN_SDATA_IN 17
#define PIN_LE 6 

#define SEL_RD 0
#define SEL_RC 1
#define SEL_TD 2
#define SEL_TC 3

inline void signalDelay(void)
{
  delayMicroseconds(5L);
}

inline void setSelect(int reg)
{
  digitalWrite(PIN_REG0, reg & 0x02);
  digitalWrite(PIN_REG1, reg & 0x01);
}

inline unsigned char readByte(int reg)
{
  unsigned char value = 0;

  setSelect(reg);
  signalDelay();

  digitalWrite(PIN_LE, 1);
  digitalWrite(PIN_SHCLK, 1);
  signalDelay();
  digitalWrite(PIN_SHCLK, 0);
  digitalWrite(PIN_LE, 0);

  int i;
  for (i=7; i>=0; i--) {
    digitalWrite(PIN_SHCLK, 1);
    signalDelay();
    digitalWrite(PIN_SHCLK, 0);
    signalDelay();
    value += digitalRead(PIN_SDATA_IN) << i;
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
  setSelect(reg);

  int i;
  for (i=7; i>=0; i--) {
    digitalWrite(PIN_SDATA_OUT, (value >> i) & 0x01);
    signalDelay();
    digitalWrite(PIN_SHCLK, 1);
    signalDelay();
    digitalWrite(PIN_SHCLK, 0);
    signalDelay();
  }

  digitalWrite(PIN_LE, 1);
  digitalWrite(PIN_SHCLK, 1);
  signalDelay();
  digitalWrite(PIN_SHCLK, 0);
  digitalWrite(PIN_LE, 0);
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
  wiringPiSetupGpio();

  pinMode(PIN_REG0, OUTPUT);
  pinMode(PIN_REG1, OUTPUT);
  pinMode(PIN_SHCLK, OUTPUT);
  pinMode(PIN_SDATA_OUT, OUTPUT);
  pinMode(PIN_LE, OUTPUT);
  pinMode(PIN_SDATA_IN, INPUT);
  pullUpDnControl(PIN_SDATA_IN, PUD_OFF);

  digitalWrite(PIN_REG0, 0);
  digitalWrite(PIN_REG1, 0);
  digitalWrite(PIN_SHCLK, 0);
  digitalWrite(PIN_SDATA_OUT, 0);
  digitalWrite(PIN_LE, 0);

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

PyMODINIT_FUNC
inittipiports(void)
{
  PyObject *m;
  m = Py_InitModule("tipiports", TipiMethods);
  if (m == NULL)
    return;
}

