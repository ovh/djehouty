#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""
import logging
from logging.handlers import SocketHandler
import ssl
import select
from djehouty import PY3

class TCPSocketHandler(SocketHandler):
    """TCPSocketHandler"""
    def __init__(self, host, port=12201, use_tls=False, cert_reqs=ssl.CERT_NONE, ca_certs=None, sock_timeout=1, level=logging.NOTSET):
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
            return ssl.wrap_socket(sock, cert_reqs=self.cert_reqs, ca_certs=self.ca_certs)
        return sock

    def checkSocket(self):
        """checkSocket"""
        try:
            r, w, e = select.select([self.sock], (), (), 0)
            if len(r) > 0:
                data = bytearray(1024)
                nb = r[0].recv_into(data, 1024)
                if nb==0:
                    return False
            return True
        except Exception as err:
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
            s = self.makePickle(record)
            if PY3:
                self.send(bytes(s, 'UTF-8'))
            else:
                self.send(s)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            # Trying to solve https://interne.gmail.com/projects/browse/LOGS-224
            # RuntimeError: maximum recursion depth exceeded'.
            # self.handleError(record)
            # dropping record atm
            pass

    def makePickle(self, record):
        """makePickle"""
        return self.format(record) + "\n"
