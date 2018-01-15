import os
import logging
import inotify.adapters
import sqlite3
import ConfigLogging
import tipi_cache
from ti_files import ti_files
from tinames import tinames

#
# Monitor file changes under tipi_disk, and update meta-data in a database
# to speed up web management
#

logger = logging.getLogger('tipi_monitor')
tipi_disk = '/home/tipi/tipi_disk'


def main():
    ConfigLogging.configure_logging()
    tipi_cache.setupSchema()
    # tipi_cache.deleteMissing()

    i = inotify.adapters.InotifyTree(tipi_disk)

    for event in i.event_gen():
        if event is not None:
            (header, type_names, watch_path, filename) = event
            if 'IN_DELETE' in type_names:
                name = os.path.join(watch_path.decode('utf-8'), filename.decode('utf-8'))
                tipi_cache.deleteFileInfo(name)
            elif 'IN_CLOSE_WRITE' in type_names:
                name = os.path.join(watch_path.decode('utf-8'), filename.decode('utf-8'))
                tipi_cache.updateFileInfo(name)

if __name__ == '__main__':
    main()

