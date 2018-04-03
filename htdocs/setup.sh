#!/bin/bash

if [ -d ENV ]; then
  rm -r ENV
fi

virtualenv --system-site-packages ENV

. ./ENV/bin/activate

pip install -r requirements.txt

