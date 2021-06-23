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

LONG_DESCRIPTION = 'Super Asset Management Service'

install_requires = [
    'superdesk-core>=2.2.0',
    'sams-client>=0.2.3,<0.3',
]

setup(
    name='sams-server',
    version='0.2.4',
    description='Super Asset Management Service',
    long_description=LONG_DESCRIPTION,
    author='Mark Pittaway',
    author_email='mark.pittaway@sourcefabric.org',
    url='https://github.com/superdesk/sams',
    license='AGPLv3',
    platforms=['any'],
    packages=find_packages(exclude=['tests']),
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
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
        'Programming Language :: Python :: 3.8',
        'Topic :: Database',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Multimedia'
    ],
    python_requires='~=3.6'
)
