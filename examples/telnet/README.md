# ANSI Terminal for TI-99/4A 

This uses TIPI TCP support to implement TELNET, with an ANSI terminal emulation.

The 80 column color mode uses a fork of Tursi's libti99:

```
https://github.com/jedimatt42/libti99
```

The 80 column mode requires F18A as it uses F18A color mode and gpu assisted
scrolling.

thanks to PeteE:

* accelerated scroll 
* color 80 column mode
* 64 column mode


