import logging
import sys

logging.basicConfig(level=logging.DEBUG)


def error(message: str):
    logging.error(message)


def info(message: str):
    logging.info(message)


def debug(message: str):
    logging.debug(message)


def warning(message: str):
    logging.warning(message)


def fatal(message: str, code: int):
    logging.fatal(message)
    sys.exit(code)
