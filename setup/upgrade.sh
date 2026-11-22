#!/bin/bash

##
## Display current and latest version available.
## Run with --upgrade to upgrade to latest
##

TIPI_REPO=${TIPI_REPO:-${TIPI_HOME:-/home/tipi}/tipi}

if [ -f $TIPI_REPO/branch.txt ]; then
  branch=`cat $TIPI_REPO/branch.txt | sed -n 's/^branch=\(.*\)$/\1/p'`
else
  branch=`cat $TIPI_REPO/version.txt | sed -n 's/^branch=\(.*\)$/\1/p'`
fi
version=`cat $TIPI_REPO/version.txt | sed -n 's/^version=\(.*\)$/\1/p'`

## I want deprecate the 'unstable' branch
if [ "$branch" = "unstable" ]; then
  branch=release
fi

remoteversion=`curl https://raw.githubusercontent.com/jedimatt42/tipi/$branch/version.txt 2>/dev/null | sed -n 's/^version=\(.*\)$/\1/p'`

echo "Current Version: $version"
echo "Latest Version: $remoteversion"

if [ "${1:-}" = "--upgrade" ]; then
  # create a child process, and upgrade all the tipi code out from under ourselves.
  # then run the new post-upgrade.sh script
  ( cd /home/tipi/tipi && su tipi -c "git fetch && git checkout $branch && git pull" && exec bash -x /home/tipi/tipi/setup/post-upgrade.sh $version)
fi
