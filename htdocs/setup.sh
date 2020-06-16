#!/bin/bash

if [ -d ENV ]; then
  rm -r ENV
fi

virtualenv --python=python3 --system-site-packages ENV

. ./ENV/bin/activate

pip install -r requirements.txt

