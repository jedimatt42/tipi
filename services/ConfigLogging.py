import logging

def configure_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    ch = logging.StreamHandler()

    logFormat = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(logFormat)
    ch.setFormatter(formatter)

    logger.addHandler(ch)


