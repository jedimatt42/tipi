# Custom Message Type Examples

To use one of these, you must install it in the `TIPI.PLUGINS` folder on the PI. That is `/home/tipi/tipi_disk/PLUGINS` from linux.

Files in the `TIPI.PLUGINS` folder should be named based on the message type they will respond to. 

So, to use `example.py` as message type 0x60, you would install it with the name `60.py`

4A programs can install custom plugins directly using the native file writing directive.

## base_example.py

This 