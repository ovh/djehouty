#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""
import sys
import socket
import logging
import json
from djehouty import SYSLOG_LEVELS

PY3 = sys.version_info[0] == 3

if PY3:
    string_type = str
    integer_type = (int,)
    base_types = (Exception, str, int, bool, float)
else:
    string_type = basestring
    integer_type = (int, long)
    base_types = (Exception, str, int, bool, float, unicode)

class GELFFormatter(logging.Formatter):
    """GELFFormatter"""

    default_fields = {
        'created'       : 'timestamp',
        'name'          : '_facility',
        'filename'      : '_file',
    }
    
    def __init__(self, static_fields=dict(), null_character=False):
        super(GELFFormatter, self).__init__()
        self.static_fields = static_fields
        self.hostname = socket.gethostname()
        self.null_character = null_character
   
    def format(self, record):
        """docstring for format"""
        rec  = dict(vars(record))
        rec.update(**self.static_fields)
        data = dict(
            version         = "1.1",
            host            = self.hostname,
            short_message   = record.getMessage(),
            level           = SYSLOG_LEVELS.get(rec.pop('levelno')),
        )
        
        # we removed args 
        map(rec.pop, ('args',))

        for attr, value in rec.items():
            key = self.default_fields[attr] if attr in self.default_fields.keys() else "_%s" % attr
            if isinstance(value, (string_type, float) + integer_type) or value is None:
                data[key] = value
            else:
                try:
                    data[key] = repr(value)
                except:
                    pass
        
        out = json.dumps(data)
        if self.null_character == True:
            out += '\0'
        return out
