#!/bin/bash

virtualenv --system-site-packages ENV

. ./ENV/bin/activate

( cd libtipi; python ./setup.py install )

pip install -r requirements.txt

