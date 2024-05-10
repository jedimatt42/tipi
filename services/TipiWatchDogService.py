#!/usr/bin/env python3

from subprocess import call

import select

tipi_reset='/dev/tipi_reset'

def restart_tipi_service():
  print("responding to reset interrupt")
  callargs = ["/bin/systemctl", "restart", "tipi.service"]
  if call(callargs) != 0:
    print("Error requesting restart of tipi.service")
  else:
    print("tipi.service restart requested")

def use_interrupt_polling():
  with open(tipi_reset, 'r') as dev_reset:
    poller = select.poll()
    poller.register(dev_reset, select.POLLIN | select.POLLERR )

    print("Waiting for RESET event...")
    while True:
      poller.poll()
      restart_tipi_service()

use_interrupt_polling()


