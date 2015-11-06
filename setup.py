#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""

from setuptools import setup, find_packages

version = '0.1.0'

setup(
    name                = 'djehouty',
    version             = version,
    description         = "Djehouty is intended to be a set of logging formatters and handlers to easly send log entries.",
    long_description    = """""",
    classifiers         = [
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
    ],
    keywords            = 'GELF, LTSV',
    author              = 'Cedric DUMAY',
    author_email        = 'cedric.dumay@gmail.com',
    url                 = 'https://github.com/cdumay/djehouty',
    license             = 'BSD',
    packages            = find_packages('src'),
    package_dir         = {'': 'src'},
    include_package_data= True,
    zip_safe            = True,
    install_requires    = (
        'distribute',
    ),
    entry_points        = """
""",
)

