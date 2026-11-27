#!/bin/bash
#
# Run TIPI's services locally in emulation mode, without a Raspberry PI.
# See README.md in this folder. Run setup.sh once first.
#
# Starts, and restarts when they exit (as systemd does on the PI):
#   services/tipi.sh   - TIPI service, websocket for emulators on port 9901
#   htdocs/app_run.sh  - web UI on port 9900
#   htdocs/tipimon.sh  - file change monitor for the web UI
#
# Stop with Ctrl-C.
#

REPO=$(cd "$(dirname "$0")/../.." && pwd)

export TIPI_HOME=${TIPI_HOME:-$HOME/tipi}
export TIPI_REPO=$REPO
# emulation mode, even if the web UI removes .emulation
export TIPI_WEBSOCK=$REPO/htdocs
export TIPI_NO_PDF=true
# no Pi: PI.REBOOT and PI.UPGRADE restart the service instead
export TIPI_NO_PI=1

LOG=$TIPI_HOME/log

if [ ! -d "$REPO/services/ENV" ] || [ ! -d "$REPO/htdocs/ENV" ]; then
  echo "Run $REPO/emulation/local/setup.sh first."
  exit 1
fi

# what tipiboot.sh and post-upgrade.sh prepare on a PI
mkdir -p "$TIPI_HOME/tipi_disk" "$LOG" "$TIPI_HOME/.tipivars" "$TIPI_HOME/web-tmp"
if [ ! -s "$TIPI_HOME/tipi.uuid" ]; then
  python3 -c 'import uuid; print(uuid.uuid4())' >"$TIPI_HOME/tipi.uuid"
fi
if [ ! -e "$TIPI_HOME/.emulation" ]; then
  printf 'NFS_ENABLED=0\nPDF_ENABLED=0\n' >"$TIPI_HOME/.emulation"
fi
# TIPICFG and friends, without replacing the user's copies
cp -R -n "$REPO"/setup/bin/* "$TIPI_HOME/tipi_disk/" 2>/dev/null

echo "TIPI_HOME: $TIPI_HOME"
echo "logs:      $LOG"
echo "emulators: ws://localhost:9901/tipi"
echo "web UI:    http://localhost:9900"

# keep a script running, as systemd's Restart=always does
supervise() {
  while true; do
    "$1" >>"$LOG/$2.out" 2>&1
    sleep 1
  done
}

# each service runs in its own process group, so it's stopped with its children
start() {
  set -m
  supervise "$1" "$2" &
  eval "pid_$2=$!"
  set +m
}

stop() {
  local pid
  eval "pid=\$pid_$1"
  if [ -n "$pid" ]; then
    kill -TERM -- "-$pid" 2>/dev/null
    wait "$pid" 2>/dev/null
    eval "pid_$1="
  fi
}

stop_all() {
  echo "stopping TIPI"
  stop tipi
  stop tipiweb
  stop tipimon
  exit 0
}
trap stop_all INT TERM

start "$REPO/services/tipi.sh" tipi
start "$REPO/htdocs/app_run.sh" tipiweb
start "$REPO/htdocs/tipimon.sh" tipimon

# stand in for TipiSuper.py, which handles requests from the TI and the web UI
while true; do
  sleep 1
  if [ -e /tmp/tipi_restart ]; then
    echo "restarting the TIPI service"
    stop tipi
    start "$REPO/services/tipi.sh" tipi
    rm -f /tmp/tipi_restart
  fi
  for request in tipihalt tipireboot tipiupgrade tz wificonfig tipi_backup tipi_restore; do
    if [ -e /tmp/$request ]; then
      echo "ignoring $request: not supported when running locally"
      rm -f /tmp/$request
    fi
  done
done
