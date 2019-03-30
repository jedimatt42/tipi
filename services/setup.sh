#!/bin/bash

if [ -d ENV ]; then
  rm -r ENV
fi

virtualenv --system-site-packages ENV

. ./ENV/bin/activate

( cd libtipi; python ./setup.py install )

pip install -r requirements.txt

( cd /tmp; git clone https://github.com/adafruit/Adafruit_Python_GPIO.git; cd /tmp/Adafruit_Python_GPIO; git checkout 268cd87672a9203217e99f85811cf33bf1ce3081; python ./setup.py install )
( cd /tmp; git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git; cd /tmp/Adafruit_Python_SSD1306; python ./setup.py install )

