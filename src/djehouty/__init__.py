#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""
import logging
import sys

SYSLOG_LEVELS = {
    logging.CRITICAL: 2,
    logging.ERROR: 3,
    logging.WARNING: 4,
    logging.INFO: 6,
    logging.DEBUG: 7,
}

PY3 = sys.version_info[0] == 3

if PY3:
    STRING_TYPE = str
    INTEGER_TYPE = (int,)
    BASE_TYPES = (Exception, str, int, bool, float)
else:
    STRING_TYPE = basestring
    INTEGER_TYPE = (int, long)
    BASE_TYPES = (Exception, str, int, bool, float, unicode)
