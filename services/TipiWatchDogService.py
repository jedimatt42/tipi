#!/usr/bin/env python3

from subprocess import call

import select
import os
import time

tipi_reset='/sys/devices/platform/tipi_gpio/tipi-reset/'

with open(tipi_reset + '/active_low', 'w') as edge:
  edge.write('0')
with open(tipi_reset + '/edge', 'w') as edge:
  edge.write('falling')

with open(tipi_reset + '/value', 'r') as reset_value:
  poller = select.poll()
  poller.register(reset_value, select.POLLPRI | select.POLLERR )

  poller.poll(-1)
  reset_value.seek(0)
  reset_value.read(1)

  print("Waiting for RESET event...")
  while True:
    poller.poll(10000)
    reset_value.seek(0)
    if reset_value.read(1) == '0':
      print("responding to reset interrupt")
      callargs = ["/bin/systemctl", "restart", "tipi.service"]
      if call(callargs) != 0:
        print("Error requesting restart of tipi.service")


