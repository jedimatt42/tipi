
#include <Python.h>
#include "gpio.h"

// Serial output for RD & RC
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

void setInput(int pin)
{
  INP_GPIO(pin);
}

void setOutput(int pin)
{
  INP_GPIO(pin);
  OUT_GPIO(pin);
}

inline unsigned char getBit(int pin)
{
  return GET_GPIO(pin) ? 1 : 0;
}

inline void setBit(int set, int pin)
{
  *(gpio + (set ? 7 : 10)) = 1<<pin;
}

inline unsigned char readByte(int reg)
{
  unsigned char value = 0;

  GPIO_SET = 1<<PIN_REG0;
  setBit(reg & 0x01, PIN_REG1);
  
  GPIO_SET = 1<<PIN_LE;
  GPIO_SET = 1<<PIN_SHCLK;
  GPIO_CLR = 1<<PIN_LE;
  GPIO_CLR = 1<<PIN_SHCLK;

  int i;
  for (i=7; i>=0; i--) {
    value += getBit(PIN_SDATA_IN) << i;
    GPIO_SET = 1<<PIN_SHCLK;
    GPIO_CLR = 1<<PIN_SHCLK;
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
  GPIO_CLR = 1<<PIN_REG0;
  setBit(reg & 0x01, PIN_REG1);

  int i;
  for (i=7; i>=0; i--) {
    GPIO_CLR = 1<<PIN_SHCLK;
    setBit((value >> i) & 0x01, PIN_SDATA_OUT);
    GPIO_SET = 1<<PIN_SHCLK;
  }
  GPIO_CLR = 1<<PIN_SHCLK;
  GPIO_SET = 1<<PIN_LE;
  GPIO_SET = 1<<PIN_SHCLK;
  GPIO_CLR = 1<<PIN_LE;
  GPIO_CLR = 1<<PIN_SHCLK;
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
  setup_io();

  setOutput(PIN_REG0);
  setOutput(PIN_REG1);
  setOutput(PIN_SHCLK);
  setOutput(PIN_SDATA_OUT);
  setInput(PIN_SDATA_IN);
  setOutput(PIN_LE);

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

