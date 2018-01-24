#!/bin/bash

if [ ! -d ENV ]; then
  virtualenv --system-site-packages ENV
fi

. ./ENV/bin/activate

pip install -r requirements.txt

