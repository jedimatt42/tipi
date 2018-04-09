# ANSI Terminal for TI-99/4A 

This uses TIPI TCP support to implement TELNET, with an ANSI terminal emulation.

The 80 column color mode uses a fork of libti99:

```
git@github.com:peberlein/libti99.git
```

The 80 column mode requires F18A, it uses features beyond 9938, thanks to PeteE:

* accelerated scroll 
* color 80 column mode
* 64 column mode

