
#include <Python.h>
#include "gpio.h"

// Used to recognize a reset request
#define PIN_RESET 5

// 8 bit bus for TI Data (TD)
#define PIN_TD0 2
#define PIN_TD1 3
#define PIN_TD2 4
#define PIN_TD3 17
#define PIN_TD4 27
#define PIN_TD5 22
#define PIN_TD6 10
#define PIN_TD7 9

// 8 bit bus for TI Control (TC)
#define PIN_TC0 14
#define PIN_TC1 15
#define PIN_TC2 18
#define PIN_TC3 23
#define PIN_TC4 24
#define PIN_TC5 25
#define PIN_TC6 8 
#define PIN_TC7 7

// Serial output for RD & RC
#define PIN_CCLK 19
#define PIN_DCLK 26
#define PIN_SDATA 13
#define PIN_LE 6 

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

static PyObject* 
tipi_getTD(PyObject *self, PyObject *args)
{
  unsigned char td_value =
    getBit(PIN_TD0) +
    (getBit(PIN_TD1) << 1) +
    (getBit(PIN_TD2) << 2) +
    (getBit(PIN_TD3) << 3) +
    (getBit(PIN_TD4) << 4) +
    (getBit(PIN_TD5) << 5) +
    (getBit(PIN_TD6) << 6) +
    (getBit(PIN_TD7) << 7);

  return Py_BuildValue("i", td_value);
}

static PyObject* 
tipi_getTC(PyObject *self, PyObject *args)
{
  unsigned char tc_value =
    getBit(PIN_TC0) +
    (getBit(PIN_TC1) << 1) +
    (getBit(PIN_TC2) << 2) +
    (getBit(PIN_TC3) << 3) +
    (getBit(PIN_TC4) << 4) +
    (getBit(PIN_TC5) << 5) +
    (getBit(PIN_TC6) << 6) +
    (getBit(PIN_TC7) << 7);

  return Py_BuildValue("i", tc_value);
}

inline void setBit(int set, int pin)
{
  *(gpio + (set ? 7 : 10)) = 1<<pin;
}

inline void writeByte(unsigned char value, int clock) 
{
  int i;
  for (i=7; i>=0; i--) {
    GPIO_CLR = 1<<clock;
    setBit((value >> i) & 0x01, PIN_SDATA);
    GPIO_SET = 1<<clock;
  }
  GPIO_CLR = 1<<clock;
  GPIO_SET = 1<<PIN_LE;
  GPIO_SET = 1<<clock;
  GPIO_CLR = 1<<PIN_LE;
  GPIO_CLR = 1<<clock;
}

static PyObject* 
tipi_setRD(PyObject *self, PyObject *args)
{
  unsigned char rd_value;
  PyArg_ParseTuple(args, "b", &rd_value);

  writeByte(rd_value, PIN_DCLK);

  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject* 
tipi_setRC(PyObject *self, PyObject *args)
{
  unsigned char rc_value;
  PyArg_ParseTuple(args, "b", &rc_value);

  writeByte(rc_value, PIN_CCLK);

  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject* 
tipi_initGpio(PyObject *self, PyObject *args)
{
  setup_io();

  setInput(PIN_TD0);
  setInput(PIN_TD1);
  setInput(PIN_TD2);
  setInput(PIN_TD3);
  setInput(PIN_TD4);
  setInput(PIN_TD5);
  setInput(PIN_TD6);
  setInput(PIN_TD7);

  setInput(PIN_TC0);
  setInput(PIN_TC1);
  setInput(PIN_TC2);
  setInput(PIN_TC3);
  setInput(PIN_TC4);
  setInput(PIN_TC5);
  setInput(PIN_TC6);
  setInput(PIN_TC7);

  setOutput(PIN_CCLK);
  setOutput(PIN_DCLK);
  setOutput(PIN_SDATA);
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

