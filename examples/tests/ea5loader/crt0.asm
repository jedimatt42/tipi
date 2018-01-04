 def _start

# burnin version
_start:
  limi 0       # Disable interrupts
  lwpi >8300   # Set initial workspace
# Create stack
  li sp, >4000
# Enter C environment
  b @main

