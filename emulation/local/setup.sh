#!/bin/bash
#
# Set up TIPI's services to run locally (macOS or Linux) in emulation mode,
# without a Raspberry PI. See README.md in this folder.
#
# Creates the Python environments services/ENV and htdocs/ENV, and clones
# xdt99 into $TIPI_HOME/xdt99. Run it again after updating this checkout.
#

set -o errexit

REPO=$(cd "$(dirname "$0")/../.." && pwd)
TIPI_HOME=${TIPI_HOME:-$HOME/tipi}
PYTHON=${PYTHON:-python3}

echo "TIPI checkout: $REPO"
echo "TIPI_HOME:     $TIPI_HOME"
echo "Python:        $(command -v $PYTHON) ($($PYTHON --version 2>&1))"

cd "$REPO"
if [ ! -d services/libtipi_web/sha1 ]; then
  ( cd services/libtipi_web; git clone https://github.com/clibs/sha1.git )
fi

make_env() {
  rm -rf ENV
  $PYTHON -m venv ENV
  . ENV/bin/activate
  pip install --quiet --upgrade pip setuptools wheel
}

# services: the websocket port library and the services' requirements
( cd services
  make_env
  echo "installing tipiports_websocket"
  pip install --quiet ./libtipi_web
  pip install --quiet -r requirements.txt
  # comes from the system site-packages on a Raspberry PI
  pip install --quiet pyyaml
)

# htdocs: the web UI and the file monitor
( cd htdocs
  make_env
  pip install --quiet -r requirements.txt
)

# xdt99 converts BASIC programs and reads disk images
if [ ! -d "$TIPI_HOME/xdt99" ]; then
  mkdir -p "$TIPI_HOME"
  git clone https://github.com/endlos99/xdt99.git "$TIPI_HOME/xdt99"
fi

echo
echo "Done. Start TIPI with: $REPO/emulation/local/run.sh"
