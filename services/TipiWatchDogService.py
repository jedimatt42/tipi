#!/usr/bin/env python3

from subprocess import call

import select
import os
import time

tipi_reset='/sys/devices/platform/tipi_gpio/tipi-reset/'

def restart_tipi_service():
  print("responding to reset interrupt")
  callargs = ["/bin/systemctl", "restart", "tipi.service"]
  if call(callargs) != 0:
    print("Error requesting restart of tipi.service")

def use_interrupt_polling():
  with open(tipi_reset + 'value', 'r') as f_reset_value:
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
        restart_tipi_service()

def use_hot_polling():
  with open(tipi_reset + 'value', 'r') as f_reset_value:
    print("Waiting for RESET event...")
    triggered = False
    while True:
      time.sleep(0.1)
      f_reset_value.seek(0)
      if f_reset_value.read(1) == '0':
        triggered = True
      else:
        if triggered:
          triggered = False
          restart_tipi_service()

with open(tipi_reset + 'active_low', 'w') as f_active_low:
  f_active_low.write('0')

try: 
  with open(tipi_reset + 'edge', 'w') as f_edge:
    f_edge.write('falling')
  use_interrupt_polling()
except:
  print("WARN: could not set trigger on falling edge")
  use_hot_polling()


