#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""
import logging

class LTSVLoggerAdapter(logging.LoggerAdapter):
    """LTSVLoggerAdapter"""
    def __init__(self, logger):
        logging.LoggerAdapter.__init__(self, logger, {})

    def process(self, msg, kwargs):
        """process"""
        new_kwargs = {}
        for attr in ('exc_info', 'extra'):
            if attr in kwargs:
                new_kwargs[attr] = kwargs.pop(attr)

        new_msg = '{0}\t{1}'.format(
            msg,
            '\t'.join('{0}:{1}'.format(*i) for i in kwargs.items()),
        )

        return new_msg, new_kwargs
