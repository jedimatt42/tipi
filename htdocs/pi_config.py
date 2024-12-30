import os
import time

from TipiConfig import TipiConfig

tipi_config = TipiConfig.instance()

def data():
    return {
        "data": [(key, tipi_config.get(key)) for key in tipi_config.keys()]
    }


def update(updated_config):
    for key, value in updated_config.items():
        tipi_config.set(key, value)
    tipi_config.save()

