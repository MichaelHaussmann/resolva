"""
This file is part of resolva.
(C) copyright 2024 Michael Haussmann, spil@xeo.info
resolva is free software and is distributed under the MIT License. See LICENSE file.
"""
import logging
import sys

log = logging.getLogger("resolva")

__detail = '[%(asctime)s] %(levelname)-8s| [%(module)s.%(funcName)s] %(message)-80s (%(lineno)d)'
__simple = '[%(asctime)s] %(levelname)-10s| %(message)-80s (%(lineno)d)'
__short = '%(levelname)-7s|  %(message)-80s (%(lineno)d)'

_handler = logging.StreamHandler(sys.stdout)
_handler.setFormatter(logging.Formatter(fmt=__short))
log.addHandler(_handler)

log.setLevel(logging.INFO)  # FIXME: config_name (depending on deploy dir)

# shortcut for users of custom "log"
from logging import DEBUG as _DEBUG, INFO as _INFO, WARNING as _WARNING, ERROR as _ERROR
log.DEBUG = _DEBUG
log.INFO = _INFO
log.WARNING = _WARNING
log.ERROR = _ERROR


class ResolvaException(Exception):
    """
    A resolva Exception.
    """


if __name__ == "__main__":

    log.debug("debug")
    log.info("info")
    log.error("error")