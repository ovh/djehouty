#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""
import logging
import socket
import datetime
import time
from djehouty import STRING_TYPE, INTEGER_TYPE
from djehouty.ltz import LTZ
from djehouty import SYSLOG_LEVELS

class LTSVFormatter(logging.Formatter):
    """"""
    default_fields = {
        'created': 'time',
        'name': 'facility',
    }

    default_datefmt = '%Y-%m-%dT%H:%M:%S.%fZ'

    def __init__(self, static_fields=dict(), null_character=False):
        super(LTSVFormatter, self).__init__()
        self.static_fields = static_fields
        self.static_fields.update(
            host    = socket.gethostname()
        )    
        self.null_character = null_character

    def format(self, record):
        """docstring for format"""
        rec  = dict(vars(record))
        rec.update(self.static_fields)

        created = datetime.datetime.utcfromtimestamp(rec.pop('created'))
        data = dict(
            message = record.getMessage(),
            level   = SYSLOG_LEVELS.get(record.levelno, record.levelno),
            time    = datetime.datetime.strftime(created, self.default_datefmt)
        )

        # we removed args 
        map(rec.pop, ('args',))

        for attr, value in rec.items():
            key = self.default_fields[attr] if attr in self.default_fields.keys() else attr
            if isinstance(value, (STRING_TYPE, float) + INTEGER_TYPE):
                data[key] = value
            elif value is None:
                data[key] = ""
            else:
                data[key] = repr(value)

        out = "\t".join('{0}:{1}'.format(*i) for i in data.items())
        if self.null_character == True:
            out += '\0'
        return out
