#!/usr/bin/env python
# -*- coding: utf-8; -*-
#
# This file is part of SAMS.
#
# Copyright 2020 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

LONG_DESCRIPTION = 'Super Asset Management Service Client'

install_requires = [
    'setuptools==36.6.0',
    'requests==2.21.0'
]

setup(
    name='sams-client',
    version='0.0.1.dev2',
    description='Super Asset Management Service Client',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Tanuj Soni',
    author_email='tanuj.soni@sourcefabric.org',
    url='https://github.com/superdesk/sams',
    license='AGPLv3',
    platforms=['any'],
    packages=find_packages(exclude=['tests']),
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Database',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Multimedia'
    ],
    python_requires='~=3.5'
)
