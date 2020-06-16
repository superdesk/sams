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

LONG_DESCRIPTION = 'Super Asset Management Service'

install_requires = [
    'eve==1.1.1',
    'eve-elastic>=7.0.0,<8.0.0',
    'flask>=1.1,<1.2',
    'flask-script>=2.0.5,<3.0',
    'gunicorn>=19.7.1',
    'honcho>=1.0.1',
]

setup(
    name='sams',
    version='0.0.1.dev1',
    description='Super Asset Management Service',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Mark Pittaway',
    author_email='mark.pittaway@sourcefabric.org',
    url='https://github.com/superdesk/sams',
    license='AGPLv3',
    platforms=['any'],
    packages=find_packages(exclude=['tests']),
    install_requires=install_requires,
    dependency_links=[
        'http://github.com/superdesk/superdesk-core/tarball/develop#egg=Superdesk-Core'
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Framework :: Flask',
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
    python_requires='~=3.6'
)
