#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""
import time
import datetime

TIMESTAMP = time.time()
TZDELTA = datetime.datetime.fromtimestamp(TIMESTAMP) - datetime.datetime.utcfromtimestamp(TIMESTAMP)

class LocalTimeZone(datetime.tzinfo):
    """LocalTimeZone"""
    def __init__(self, *args, **kw):
        super(LocalTimeZone, self).__init__(*args, **kw)
        self.tzdelta = TZDELTA

    def utcoffset(self, dt):
        """utcoffset"""
        return self.tzdelta

    def dst(self, dt):
        """dst"""
        return datetime.timedelta(0)

LTZ = LocalTimeZone()

