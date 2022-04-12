
export TIPI_DIR

if [ -f $TIPI_DIR/.tipi_settings ]; then
  source $TIPI_DIR/.tipi_settings
fi

if [ -z ${TIPI_DISK:-} ]; then
  TIPI_DISK=/home/tipi/tipi_disk
fi
if [ -z ${TIPI_CONF:-} ]; then
  TIPI_CONF=/home/tipi
fi

export TIPI_DISK
export TIPI_CONF

echo "TIPI_DIR:  $TIPI_DIR"
echo "TIPI_CONF: $TIPI_CONF"
echo "TIPI_DISK: $TIPI_DISK"

