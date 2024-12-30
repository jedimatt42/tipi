import os
import time

from TipiConfig import TipiConfig

tipi_config = TipiConfig.instance()

def data():
    return {
        "data": [(key, tipi_config.get(key)) for key in tipi_config.keys()],
        "descriptions": {
          "AUTO": "If 'on' TIPI will automatically map DSK1 to the directory that a PROGRAM image file is loaded from. This mapping only persists until the console is reset. Default 'off', valid values: on, off",
          "CS1_FILE": "Map file operations for device CS1 to the specified file. File names should be in TI format relative to the TIPI. device.",
          "CUSTOM_BINS": "Normally on reboot of the Raspberry PI, the TIPI.TIPICFG PROGRAM image files are overwritten by the shipping version of TIPICFG. Set this to 1 to prevent this so that you can replace what is loaded by CALL TIPI. Default 0, valid values: 0, 1",
          "DIR_SORT": "When reading a catalog from TIPI or a mapped drive, control the order of directory entries vs file entries. Default FIRST, valid values: MIXED, FIRST, LAST",
          "DSK1_DIR": "Map a directory on TIPI to device DSK1.",
          "DSK2_DIR": "Map a directory on TIPI to device DSK2.",
          "DSK3_DIR": "Map a directory on TIPI to device DSK3.",
          "DSK4_DIR": "Map a directory on TIPI to device DSK4.",
          "DSK5_DIR": "Map a directory on TIPI to device DSK5.",
          "DSK6_DIR": "Map a directory on TIPI to device DSK6.",
          "DSK7_DIR": "Map a directory on TIPI to device DSK7.",
          "DSK8_DIR": "Map a directory on TIPI to device DSK8.",
          "DSK9_DIR": "Map a directory on TIPI to device DSK9.",
          "EAGER_WRITE": "If set to on, TIPI will write files with each written record, otherwise it will wait until the file is closed and then write all the records. Default off, valid values: off, on",
          "HOST_EOL": "Controls end of line characters when using the ?W device name modifier. Default CRLF, valid values LF, CRLF",
          "LVL3_NOT_FOUND": "Default ERROR, valid values: PASS, ERROR",
          "MOUSE_SCALE": "Default 50, valid valids 1-100",
          "NATIVE_TEXT_DIRS": "When writing DV/80 files to the listed directories, they will be written as plain text unix files instead of TIFILES. Valid values: a comma seperated list of directories relative to the TIPI. devicename.",
          "SECTOR_COUNT": "Number of disk sectors to report as the disk size. Default 1440, valid values: 2-65536",
          "TIPI_NAME": "Ignored.",
          "TZ": "Timezone for setting the Raspberry PI clock. https://github.com/jedimatt42/tipi/wiki/timezones",
          "URI1": "Use to extend http(s) file path access for long URLs",
          "URI2": "Use to extend http(s) file path access for long URLs",
          "URI3": "Use to extend http(s) file path access for long URLs",
          "WIFI_PSK": "Set the Raspberry PI WIFI password/preshared key.",
          "WIFI_SSID": "Set the SSID of the Raspberry PI WIFI.",
        }
    }


def update(updated_config):
    for key, value in updated_config.items():
        tipi_config.set(key, value)
    tipi_config.save()

