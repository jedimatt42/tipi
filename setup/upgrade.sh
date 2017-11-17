#!/bin/bash

##
## Display current and latest version available.
## Run with --upgrade to upgrade to latest
##

branch=`cat /home/tipi/tipi/version.txt | sed -n 's/^branch=\(.*\)$/\1/p'`
version=`cat /home/tipi/tipi/version.txt | sed -n 's/^version=\(.*\)$/\1/p'`

remoteversion=`curl https://raw.githubusercontent.com/jedimatt42/tipi/$branch/version.txt 2>/dev/null | sed -n 's/^version=\(.*\)$/\1/p'`

echo "Current Version: $version"
echo "Latest Version: $remoteversion"

if [ "${1:-}" = "--upgrade" ]; then
  # create a child process, and upgrade all the tipi code out from under ourselves.
  # then run the new post-upgrade.sh script
  ( cd /home/tipi/tipi && git checkout $branch && git pull && exec bash -x /home/tipi/tipi/setup/post-upgrade.sh )
fi