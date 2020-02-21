#!/usr/bin/env python

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name                          = 'ssm-loader',
    version                       = '0.1',
    py_modules                    = ['ssm'],
    include_package_data          = True,
    description                   = 'Python app to load SSM',
    long_description              = long_description,
    long_description_content_type = "text/markdown",
    author                        = 'DNX Solutions',
    author_email                  = 'contact@dnx.solutions',
    python_requires               = '>=3.6',
    entry_points='''
        [console_scripts]
        ssm=ssm:cli
    ''',
)