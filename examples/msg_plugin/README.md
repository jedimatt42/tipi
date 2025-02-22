# Custom Message Type Examples

To use one of these, you must install it in the `TIPI.PLUGINS` folder on the PI. That is `/home/tipi/tipi_disk/PLUGINS` from linux.

Files in the `TIPI.PLUGINS` folder should be named based on the message type they will respond to. 

So, to use `example.py` as message type 0x60, you would install it with the name `60.py`

4A programs can install custom plugins directly using the native file writing directive.

## base_example.py

This example shows a handler for a single byte message that contains only the message type. The framework will only send messages to
the plugin if the installed name matches the message type byte. So this can be ignored. 

Upon receipt, the handler returns the 'A' as a byte array.

All plugins should return an array of bytes. It may be an empty array. 

All interactions with plugins are of the sequence: write message to plugin, read response message from plugin.

## keyboard.py

This is a keyboard handler, much like the built-in mouse extension. There is a rough handling of the USB events for the keyboard, and 
they are translated to ascii terminal codes. It is incomplete. The example handles a-z, 0-9, basic punctuation, capitalization with shift and keycaps, and control keys. 

This example grabs the linux keyboard on first use. The keyboard is freed when the `tipi.service` is restarted, such as when the 4A is rebooted. 