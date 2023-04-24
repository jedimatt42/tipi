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
import re
from ti_files import ti_files
from tinames import tinames

LOGGER = logging.getLogger(__name__)

CONFIG_DEFAULTS = {
    "AUTO": "off",
    "DSK1_DIR": "",
    "DSK2_DIR": "",
    "DSK3_DIR": "",
    "DSK4_DIR": "",
    "URI1": "",
    "URI2": "",
    "URI3": "",
    "TIPI_NAME": "TIPI",
    "WIFI_SSID": "",
    "WIFI_PSK": "",
    "MOUSE_SCALE": "50",
    "TZ": "America/Los_Angeles",
    "SECTOR_COUNT": "1440",
    "DIR_SORT": "FIRST",
    "EAGER_WRITE": "off",
    "HOST_EOL": "CRLF",
    "NATIVE_TEXT_DIRS": "",
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
            key = str(line).split("=")[0].strip()
            value = str(line).split("=")[1].strip()
            self.records[key] = value
            LOGGER.debug("read record: %s = %s", key, value)
        self.sorted_keys = list(self.records.keys())
        self.sorted_keys.sort()

    def load(self):
        """ read config values from file """
        if os.path.exists(self.tipi_config):
            self.mtime = os.path.getmtime(self.tipi_config)
            self.records = dict(CONFIG_DEFAULTS)
            with open(self.tipi_config, "r") as in_file:
                self.applyrecords(in_file.readlines())
        else:
            LOGGER.info("config file missing: %s", self.tipi_config)

    def save(self):
        """ write the in-memory config out to disk to share and persist """
        with open(self.tipi_config, "w") as out_file:
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
            newvalue = self.__sanitizeValue(key, newvalue)
            self.records[key] = newvalue
            self.sorted_keys = list(self.records.keys())
            self.sorted_keys.sort()
            self.changes.add(key)

    def settmp(self, key, value):
        """ Update item, but do not add to changes. """
        value = self.__sanitizeValue(key, value)
        self.records[key.strip()] = value.strip()

    def get(self, key, default=None):
        """ Fetch a config item """
        self.__check_for_update()
        return self.records.get(key.strip(), default)

    def __triggerWifiConfig(self):
        with open("/tmp/wificonfig", "w") as out_file:
            out_file.write(self.records["WIFI_SSID"])
            out_file.write("\n")
            out_file.write(self.records["WIFI_PSK"])
            out_file.write("\n")

    def __triggerTimezone(self):
        with open("/tmp/tz", "w") as out_file:
            out_file.write(self.records["TZ"])
            out_file.write("\n")
        while os.path.exists("/tmp/tz"):
            time.sleep(0.5)

    def __sanitizeValue(self, key, newvalue):
        if key.endswith("_DIR"):
            return self.__sanitizeMapping(newvalue)
        if key == "NATIVE_TEXT_DIRS":
            return self.__sanitizeDirList(newvalue)
        return newvalue

    def __sanitizeDirList(self, newvalue):
        if newvalue.strip() == "":
            return ""
        items = newvalue.split(',')
        clean_list = []
        for dir in items:
            # if the user includes the TIPI. device prefix, remove it for them.
            # unless they actually have a TIPI. directory
            if dir.startswith("TIPI.") and not os.path.isdir("/home/tipi/tipi_disk/TIPI"):
                dir = dir[5:]
            # if the user does not include the trailing directory separator, add it for them.
            if dir and not dir.endswith("."):
                dir = f"{dir}."
            clean_list.append(dir)
        return ','.join(clean_list)

    def __sanitizeMapping(self, newvalue):
        if newvalue == "." or newvalue == "TIPI." or newvalue == "TIPI":
            return "."
        newvalue = re.sub("[.]+", ".", newvalue)
        if newvalue.endswith("."):
            newvalue = newvalue[:-1]
        if newvalue.startswith("."):
            newvalue = newvalue[1:]
        if newvalue.startswith("TIPI."):
            newvalue = newvalue[5:]
        return newvalue


SINGLETON = TipiConfig()
