
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


char* errorsFifo = "/tmp/tipierrors";

void writeErrors(int errors) {
  int fd = open(errorsFifo, O_WRONLY);
  write(fd, (void*)&errors, 2);
  close(fd);
}

static PyObject* (*readMsg)(void);
static PyObject* (*sendMsg)(unsigned char *, int);
static PyObject* (*sendMouseEvent)(void);


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
  "tipiports_websocket",
  NULL, /* module documentation */
  -1,  /* global variable state */
  TipiMethods
};

PyMODINIT_FUNC
PyInit_tipiports_websocket(void)
{
  return PyModule_Create(&TipiModule);
}
