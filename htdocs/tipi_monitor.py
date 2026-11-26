import os
import logging
try:
    import inotify.adapters
except ImportError:
    # inotify is Linux only; elsewhere (macOS) use watchfiles
    inotify = None
    from watchfiles import watch, Change
import sqlite3
import ConfigLogging
import tipi_cache
from ti_files import ti_files
from tinames import tinames
from dsks.extract_sectordump import extractDisk
from tipi_paths import TIPI_DISK
from tipi_paths import TIPI_TMP

#
# Monitor file changes under tipi_disk, and update meta-data in a database
# to speed up web management
#

logger = logging.getLogger("tipi_monitor")
tipi_disk = TIPI_DISK

tipimon_lock = os.path.join(TIPI_TMP, "tipimon.lock")


def createLock():
    lf = open(tipimon_lock, "w")
    lf.write("nonsense")
    lf.close()


def releaseLock():
    if os.path.isfile(tipimon_lock):
        os.remove(tipimon_lock)


def fileWritten(name):
    if name.lower().endswith((".dsk", ".tidisk")):
        logger.info("extracting: " + name)
        extractDisk(name)
    else:
        tipi_cache.updateFileInfo(name)


def watchfilesMonitor():
    # watchfiles reports resolved paths (on macOS /tmp is /private/tmp)
    real_disk = os.path.realpath(tipi_disk)

    logger.info("File change monitor ready (watchfiles)")

    for changes in watch(real_disk):
        createLock()
        for (change, path) in sorted(changes, key=lambda c: c[1]):
            name = tipi_disk + path[len(real_disk):]
            if change == Change.deleted:
                tipi_cache.deleteFileInfo(name)
            elif os.path.isfile(name):
                # watchfiles debounces, so the write has finished
                fileWritten(name)
        releaseLock()


def main():
    ConfigLogging.configure_logging()
    tipi_cache.setupSchema()
    tipi_cache.deleteMissing()
    tipi_cache.addAbsent()

    if inotify is None:
        watchfilesMonitor()
        return

    i = inotify.adapters.InotifyTree(tipi_disk)

    logger.info("File change monitor ready")

    for event in i.event_gen():
        if event is not None:
            createLock()
            (header, type_names, watch_path, filename) = event
            if "IN_DELETE" in type_names:
                name = os.path.join(
                    watch_path, filename
                )
                tipi_cache.deleteFileInfo(name)
            elif "IN_CLOSE_WRITE" in type_names:
                name = os.path.join(
                    watch_path, filename
                )
                fileWritten(name)
            releaseLock()


if __name__ == "__main__":
    main()
