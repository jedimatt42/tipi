import logging
import inotify.adapters

logger = logging.getLogger(__name__)

def configure_logging():
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()

    logFormat = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(logFormat)
    ch.setFormatter(formatter)

    logger.addHandler(ch)


def main():
    i = inotify.adapters.InotifyTree('/home/tipi/tipi_disk/')

    for event in i.event_gen():
        if event is not None:
            (header, type_names, watch_path, filename) = event
            if 'IN_DELETE' in type_names:
                logger.info("Deleted %s/%s", watch_path.decode('utf-8'), filename.decode('utf-8'))
            elif 'IN_CREATE' in type_names:
                logger.info("Created %s/%s", watch_path.decode('utf-8'), filename.decode('utf-8'))

if __name__ == '__main__':
    configure_logging()
    main()

