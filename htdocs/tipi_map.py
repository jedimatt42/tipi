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

