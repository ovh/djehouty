#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013-2016, OVH SAS.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#  * Neither the name of OVH SAS nor the
#    names of its contributors may be used to endorse or promote products
#    derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY OVH SAS AND CONTRIBUTORS ````AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL OVH SAS AND CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Djehouty intends to be a set of logging formatters and handlers to easily
send log entries.
"""

import socket
import logging
import json
from djehouty import SYSLOG_LEVELS, STRING_TYPE, INTEGER_TYPE

class GELFFormatter(logging.Formatter):
    """GELFFormatter"""

    default_fields = {
        'created'       : 'timestamp',
        'name'          : '_facility',
        'filename'      : '_file',
    }

    def __init__(self, static_fields=None, null_character=False):
        logging.Formatter.__init__(self)
        if static_fields is None:
            static_fields = dict()
        self.static_fields = static_fields
        self.hostname = socket.gethostname()
        self.null_character = null_character

    def format(self, record):
        """docstring for format"""
        rec = dict(vars(record))
        rec.update(**self.static_fields)
        data = dict(
            version="1.1",
            host=self.hostname,
            short_message=record.getMessage(),
            level=SYSLOG_LEVELS.get(rec.pop('levelno')),
        )

        # we removed args
        rec.pop('args')

        for attr, value in rec.items():
            if attr in self.default_fields.keys():
                key = self.default_fields[attr]
            else:
                key = "_%s" % attr
            check_str = isinstance(value, (STRING_TYPE, float) + INTEGER_TYPE)
            if check_str or value is None:
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
