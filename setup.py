#!/usr/bin/env python

try:
    from setuptools import setup

except:
    from distutils.core import setup

import muirc


setup(
    name = "muirc",
    description = "Micro IRC client",
    
    py_modules = ["muirc"],
    test_suite = "tests",

    version = muirc.__version__,
    author = muirc.__author__,
    author_email = muirc.__email__,
    url = "https://github.com/Gawen/muirc",
    license = muirc.__license__,
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Communications :: Chat",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
