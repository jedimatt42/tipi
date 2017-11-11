#!/bin/bash

branch=`cat /home/tipi/tipi/version.txt | sed -n 's/^branch=\(.*\)$/\1/p'`

# create a child process, and upgrade all the tipi code out from under ourselves.
# then run the new post-upgrade.sh script
( cd /home/tipi/tipi && git checkout $branch && git pull && exec bash -x /home/tipi/tipi/setup/post-upgrade.sh )
