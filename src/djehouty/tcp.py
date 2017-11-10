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

import logging
from logging.handlers import SocketHandler
import ssl
import select
from djehouty import PY_3

class TCPSocketHandler(SocketHandler):
    """TCPSocketHandler"""
    def __init__(self, host, port=12201, use_tls=False,
                 cert_reqs=ssl.CERT_NONE, ca_certs=None,
                 sock_timeout=1, level=logging.NOTSET):
        super(TCPSocketHandler, self).__init__(host, port)
        self.ca_certs = ca_certs
        self.cert_reqs = cert_reqs
        self.use_tls = use_tls
        self.sock_timeout = sock_timeout
        self.setLevel(level)

    def makeSocket(self):
        """makeSocket"""
        sock = SocketHandler.makeSocket(self, timeout=self.sock_timeout)
        if self.use_tls is True:
            return ssl.wrap_socket(sock, cert_reqs=self.cert_reqs, \
                   ca_certs=self.ca_certs)
        return sock

    def checkSocket(self):
        """checkSocket"""
        try:
            rlist, wlist, xlist = select.select((self.sock,), (), (), 0)
            if len(rlist) > 0:
                data = bytearray(1024)
                nbytes = rlist[0].recv_into(data, 1024)
                if nbytes == 0:
                    return False
            return True
        except:
            return False

    def emit(self, record):
        """"""
        if self.sock:
            if self.checkSocket() is False:
                try:
                    self.sock.close()
                except:
                    pass
                self.sock = None

        try:
            pickle = self.makePickle(record)
            if PY_3:
                self.send(bytes(pickle, 'UTF-8'))
            else:
                self.send(pickle)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            # RuntimeError: maximum recursion depth exceeded'.
            # self.handleError(record)
            # dropping record atm
            pass

    def makePickle(self, record):
        """makePickle"""
        return self.format(record) + "\n"
