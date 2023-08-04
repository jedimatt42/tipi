from datetime import datetime
from TipiConfig import TipiConfig

import logging

logger = logging.getLogger(__name__)

tipi_config = TipiConfig.instance()

def mapdrive(key, path, dirs):
    mapping = path[1:].replace('/', '.') + '.' + dirs[0]
    tipi_config.set(key, mapping)
    logger.info(f"mapped drive key: {key}, mapping: {mapping}")
    tipi_config.save()


def unmapdrive(key):
    tipi_config.set(key, "")
    logger.info(f"removed mapped drive key: {key}")
    tipi_config.save()


def mapfile(key, value, path=None):
    if path:
        path = path[1:].replace('/', '.')
        value = path + '.' + value if path else value
    tipi_config.set(key, value)
    logger.info(f"mapped file key: {key}, mapping: {value}")
    tipi_config.save()

