
# Native C to python interface for tipi gpio

This library should encapsulate the GPIO routines required for interacting with the 
shift registers and data latches that are in the TIPI hardware, from the Raspberry PI
side of the interface. 

Using C instead of RPi.GPIO should be able to outpace the TI-99/4A, where the python
library is relatively slow. Benchmarks from 2015 showed RPi.GPIO operating at 70 Khz, 
where Native C operated at 22 Mhz. 

With the use of shift registers, we go from 16 IOs per byte to 56 IOs per byte. 
Consequently, the need for performance is real.

# Building

```
virtualenv env
. env/bin/activate
pip install -r requirements.txt
python setup.py install
```

# Usage

Example python usage of the library.

```
import tipiports

# initialize GPIO pins for TIPI
tipiports.initGpio()

# read control byte from TI
print tipiports.getTC()

# read data byte from TI
print tipiports.getTD()

# set data byte from RPi
tipiports.setRD()

# set control byte from RPi
tipiports.setRC()
```

