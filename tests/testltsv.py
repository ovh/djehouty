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
Djehouty is intended to be a set of logging formatters and handlers to easily
send log entries.
"""

import unittest
import logging
import StringIO
import ltsv

from djehouty.libltsv.formatters import LTSVFormatter
from testfixtures import log_capture

class LTSVTestCase(unittest.TestCase):
    """ Test our LTSV formatter """

    def setUp(self):
        """"""
        self.logger = logging.getLogger('djehouty-ltsv')
        self.logger.setLevel(logging.DEBUG)
        self.buffer = StringIO.StringIO()
        self.log_handler = logging.StreamHandler(self.buffer)
        self.log_handler.setFormatter(
                 LTSVFormatter(static_fields={"app": 'djehouty-ltsv'})
        )
        self.logger.addHandler(self.log_handler)

    @log_capture()
    def test_logger(self, capture):
        """ Testing logger itself """
        self.logger.info('hello world')
        self.logger.error('Where is john doe?')
        self.logger.info('start of block number %i', 1)
        capture.check(
            ('djehouty-ltsv', 'INFO', 'hello world'),
            ('djehouty-ltsv', 'ERROR', 'Where is john doe?'),
            ('djehouty-ltsv', 'INFO', 'start of block number 1'),
        )

    def test_simple_message(self):
        """ Testing format with a common message """
        msg = "testing logging format"
        self.logger.info(msg)
        ltsv_object = ltsv.reader(self.buffer.getvalue().splitlines())
        for line in ltsv_object:
            cell = dict(line)
            self.assertEqual(cell["msg"], msg)
            self.assertEqual(cell["levelname"], "INFO")
            self.assertEqual(cell["level"], "6")
            self.assertEqual(cell["app"], "djehouty-ltsv")
            self.assertEqual(cell["funcName"], "test_simple_message")

    def test_complex_message(self):
        """ Testing format with extra values """
        msg = "testing logging format"
        self.logger.info(msg, extra={"lang": 'en', "env": 'test'})
        ltsv_object = ltsv.reader(self.buffer.getvalue().splitlines())
        for line in ltsv_object:
            cell = dict(line)
            self.assertEqual(cell["msg"], msg)
            self.assertEqual(cell["levelname"], "INFO")
            self.assertEqual(cell["level"], "6")
            self.assertEqual(cell["app"], "djehouty-ltsv")
            self.assertEqual(cell["funcName"], "test_complex_message")
            self.assertEqual(cell["lang"], "en")
            self.assertEqual(cell["env"], "test")
