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

## How to send logs

The following examples assume that you already have an Flowgger 
(see the [Flowgger documentation](https://github.com/jedisct1/flowgger/wiki) 
for more information) or a Graylog functional.

To send log messages, just use the handler of the desired format with the
following parameters:

* **host** (required): The hostname or ip address of the flowgger.
* **port** (optional): The TCP port to use (default: 12200 for GELF, 5140 for
  LTSV).
* **level** (optional): Sets the threshold for the handler (default: logging.NOTSET).
* **use_tls** (optional): Do we use TLS? (default: False).
* **cert_reqs** (optional): Specifies whether a certificate is required from the 
  other side of the connection, see  [SSL constants](https://docs.python.org/2/library/ssl.html#constants)) (default: ssl.CERT_NONE).
* **ca_certs** (optional): File that contains a set of concatenated “certification authority” certificates (default: None).
* **static_fields** (optional): Additional static fields sent with all logging.
  record (default: empty dict).
* **sock_timeout** (optional): Socket timeout is seconds (default: 1).
* **null_character** (optional): Append a null character at the end of each message (required by Graylog for GELF).

### With GELF (over TCP/TLS)
    
    import logging
    from djehouty.gelf.handlers import GELFTCPSocketHandler

    gelf_logger = logging.getLogger('djehouty-gelf')
    gelf_logger.setLevel(logging.DEBUG)
    gelf_logger.addHandler(GELFTCPSocketHandler(
        host            = "127.0.0.1", 
        port            = 5140, 
        static_fields   = {"app": 'djehouty-gelf'}, 
        use_tls         = True,
        level           = logging.DEBUG,
        null_character  = True,
    ))
    
    gelf_logger.info('test')

### With LTSV (over TCP/TLS)

    import logging
    from djehouty.ltsv.handlers import LTSVTCPSocketHandler

    ltsv_logger = logging.getLogger('djehouty-ltsv')
    ltsv_logger.setLevel(logging.DEBUG) 
    ltsv_logger.addHandler(LTSVTCPSocketHandler(
        host            = "127.0.0.1", 
        port            = 5140, 
        static_fields   = {"app": 'djehouty-ltsv'}, 
        use_tls         = True,
        level           = logging.DEBUG
    ))
    
    ltsv_logger.info('test')


## Send additional meta data

If you have many handler, you can use the [logging.LoggerAdapter](https://docs.python.org/2/library/logging.html#loggeradapter-objects) class to add
extra.

The following example uses the LTSV logger defined above:

    mylogger = logging.LoggerAdapter(
        ltsv_logger,
        extra = {"myvar": 5}
    )
    mylogger.info('test')

You can add specific log meta for each entry using the extra parameter, the following example uses the LTSV logger defined above:

    ltsv_logger.info("Hello '%s'", 'Cedric', extra={"lang": 'en'})
    ltsv_logger.info("Bonjour '%s'", 'Cedric', extra={"lang": 'fr'})

## Other transport

The formatters can be used directly, especially for debugging or write to
files.

The following example format each log record into GELF and LTSV:

    import sys
    import logging
    from djehouty.gelf.formatters import GELFFormatter
    from djehouty.ltsv.formatters import LTSVFormatter

    logger = logging.getLogger('djehouty')
    logger.setLevel(logging.DEBUG)

    # GELF
    hdr = logging.StreamHandler(sys.stdout)
    hdr.setLevel(logging.DEBUG)
    hdr.setFormatter(GELFFormatter(static_fields={"app": 'djehouty-gelf'}))
    logger.addHandler(hdr)

    # LTSV
    hdr = logging.StreamHandler(sys.stdout)
    hdr.setLevel(logging.DEBUG)
    hdr.setFormatter(LTSVFormatter(static_fields={"app": 'djehouty-ltsv'}))
    logger.addHandler(hdr)

    logger.info("Hello %s", 'cedric', extra={"lang": 'en'})

Output (GELF and LTSV):

    {"_lang": "en", "_file": "test_stdout.py", "_levelname": "INFO", "_relativeCreated": 11.034011840820312, "_processName": "MainProcess", "_thread": 140168491099904, "_exc_text": null, "_process": 28542, "version": "1.1", "_exc_info": null, "_facility": "djehouty", "short_message": "Hello cedric", "app": "djehouty-gelf", "_msecs": 308.2098960876465, "_pathname": "./test_stdout.py", "timestamp": 1440761245.30821, "_funcName": "<module>", "host": "linux-426s", "_threadName": "MainThread", "_module": "test_stdout", "level": 6, "_msg": "Hello %s", "_lineno": 30}
    relativeCreated:11.0340118408	process:28542	app:djehouty-ltsv	module:test_stdout	funcName:<module>	message:Hello cedric	facility:djehouty	filename:test_stdout.py	levelno:20	processName:MainProcess	lineno:30	msg:Hello %s	host:linux-426s	exc_text:	lang:en	thread:140168491099904	level:6	threadName:MainThread	msecs:308.209896088	pathname:./test_stdout.py	time:2015-08-28T11:27:25.308210Z	exc_info:	levelname:INFO

## License

Djehouty is availible under the [BSD 2-Clause License](https://opensource.org/licenses/BSD-2-Clause), see the `LICENSE` file for more information.
