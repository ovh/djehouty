#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""
import ssl
import logging
from djehouty.tcp import TCPSocketHandler
from djehouty.ltsv.formatters import LTSVFormatter

class LTSVTCPSocketHandler(TCPSocketHandler):
    """Graylog Extended Log Format handler using TCP
    """

    def __init__(self, host, port=5140, use_tls=False, cert_reqs=ssl.CERT_NONE, ca_certs=None, static_fields={}, sock_timeout=1, level=logging.NOTSET, null_character=False):
        super(LTSVTCPSocketHandler, self).__init__(host, port, use_tls, cert_reqs, ca_certs, sock_timeout, level)
        self.setFormatter(LTSVFormatter(static_fields, null_character=null_character))
