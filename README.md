[![Build Status](https://travis-ci.org/cdumay/djehouty.svg?branch=master)](https://travis-ci.org/cdumay/djehouty)

# Djehouty

Djehouty is intended to be a set of logging formatters and handlers to easly send log entries.

This package includes:

* for [GELF](https://www.graylog.org/resources/gelf-2/):
    
    * a TCP/TLS handler to send log entries over TCP with TLS support
    * a formatter to convert logging record into GELF(1.1).

* for [LTSV](http://ltsv.org/):
    
    * a TCP/TLS handler to send log entries over TCP with TLS support
    * a formatter to convert logging record into LTSV.

## License

Djehouty is availible under the [BSD 2-Clause License](https://opensource.org/licenses/BSD-2-Clause), see the `LICENSE` file for more information.
