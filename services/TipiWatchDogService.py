#!/usr/bin/env python3

from subprocess import call

import select
import os
import time

tipi_reset='/sys/devices/platform/tipi_gpio/tipi-reset/'

with open(tipi_reset + '/active_low', 'w') as f_active_low:
  f_active_low.write('0')
try: 
  with open(tipi_reset + '/edge', 'w') as f_edge:
    f_edge.write('falling')
except:
    print("WARN: could not set trigger on falling edge")

with open(tipi_reset + '/value', 'r') as f_reset_value:
  poller = select.poll()
  poller.register(f_reset_value, select.POLLPRI | select.POLLERR )

  poller.poll(-1)
  f_reset_value.seek(0)
  f_reset_value.read(1)

  print("Waiting for RESET event...")
  while True:
    poller.poll(10000)
    f_reset_value.seek(0)
    if f_reset_value.read(1) == '0':
      print("responding to reset interrupt")
      callargs = ["/bin/systemctl", "restart", "tipi.service"]
      if call(callargs) != 0:
        print("Error requesting restart of tipi.service")


