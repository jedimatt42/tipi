"""
This config object will be used by in process and external process
services. It is externally shared as /home/tipi/tipi.config, and
internally by providing the TipiConfig.instance() accessor.
If an external actor has updated the file it will be reloaded
automatically with any read operation (get & keys). Unsaved
data will be lost.
"""

import os
import logging
import time
from ti_files.ti_files import ti_files

LOGGER = logging.getLogger(__name__)

CONFIG_DEFAULTS = {
    "AUTO": "off",
    "DSK1_DIR": "",
    "DSK2_DIR": "",
    "DSK3_DIR": "",
    "URI1": "",
    "URI2": "",
    "URI3": "",
    "TIPI_NAME": "TIPI",
    "WIFI_SSID": "",
    "WIFI_PSK": "",
    "MOUSE_SCALE": "50",
    "OLED_ROTATE": "0",
    "TZ": "America/Los_Angeles"
}


class TipiConfig(object):
    """ Encapsulation of tipi.config file, and in memory config values """

    def __init__(self):
        self.tipi_config = "/home/tipi/tipi.config"
        self.records = dict(CONFIG_DEFAULTS)
        self.sorted_keys = []
        self.mtime = 0
        self.changes = set()
        self.load()

    @staticmethod
    def instance():
        """ return the singleton config object """
        return SINGLETON

    def applyrecords(self, records):
        for line in records:
            key = str(line).split('=')[0].strip()
            value = str(line).split('=')[1].strip()
            self.records[key] = value
            LOGGER.debug("read record: %s = %s", key, value)
        self.sorted_keys = list(self.records.keys())
        self.sorted_keys.sort()

    def load(self):
        """ read config values from file """
        if os.path.exists(self.tipi_config):
            self.mtime = os.path.getmtime(self.tipi_config)
            self.records = dict(CONFIG_DEFAULTS)
            with open(self.tipi_config, 'r') as in_file:
                self.applyrecords(in_file.readlines())
        else:
            LOGGER.info("config file missing: %s", self.tipi_config)

    def save(self):
        """ write the in-memory config out to disk to share and persist """
        with open(self.tipi_config, 'w') as out_file:
            for key in self.sorted_keys:
                out_file.write(key + "=" + self.records[key])
                out_file.write("\n")

        # Some config events require action
        if "WIFI_SSID" in self.changes or "WIFI_PSK" in self.changes:
            self.__triggerWifiConfig()
        if "TZ" in self.changes:
            self.__triggerTimezone()

        # reset changed settings
        self.changes = set()

    def __check_for_update(self):
        if os.path.exists(self.tipi_config):
            if os.path.getmtime(self.tipi_config) > self.mtime:
                self.load()

    def keys(self):
        """ Provide the keys to iterate over """
        self.__check_for_update()
        return self.sorted_keys

    def set(self, key, value):
        """ Update a config item """
        key = key.strip()
        newvalue = value.strip()
        oldvalue = self.records.get(key, "")
        if oldvalue != newvalue:
            self.records[key] = newvalue
            self.sorted_keys = list(self.records.keys())
            self.sorted_keys.sort()
            self.changes.add(key)

    def settmp(self, key, value):
        """ Update item, but do not add to changes. """
        self.records[key.strip()] = value.strip()

    def get(self, key, default=None):
        """ Fetch a config item """
        self.__check_for_update()
        return self.records.get(key.strip(), default)

    def __triggerWifiConfig(self):
        with open("/tmp/wificonfig", 'w') as out_file:
            out_file.write(self.records["WIFI_SSID"])
            out_file.write('\n')
            out_file.write(self.records["WIFI_PSK"])
            out_file.write('\n')

    def __triggerTimezone(self):
        with open("/tmp/tz", 'w') as out_file:
            out_file.write(self.records["TZ"])
            out_file.write('\n')
        while os.path.exists("/tmp/tz"):
            time.sleep(0.5)


SINGLETON = TipiConfig()
