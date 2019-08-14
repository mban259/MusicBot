from datetime import datetime
import logging
logger = logging.getLogger("log")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

sh = logging.StreamHandler()
sh.setFormatter(formatter)

fh = logging.FileHandler("data/debug.log")
fh.setFormatter(formatter)

logger.addHandler(sh)
logger.addHandler(fh)


def debug(obj):
    logger.debug(obj)


def info(obj):
    logger.info(obj)


def warning(obj):
    logger.warning(obj)


def error(obj):
    logger.error(obj)


def critical(obj):
    logger.critical(obj)
