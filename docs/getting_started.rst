===============
Getting Started
===============

.. highlight:: bash

SAMS (Super Asset Management System) is a flexible Asset management system.
It is written using the Python language, and uses
`Superdesk-Core  <https://superdesk.readthedocs.io/en/latest/>`_ as the application framework.

Requirements
============

SAMS requires access to a MongoDB and Elasticsearch instances.
The following is a list of the versions that have been tested against:

* **Python**: 3.6, 3.8
* **MongoDB**: 3.6, 4.4
* **Elasticsearch**: 7.x
* **Superdesk-Core**: 2.2, 2.3

Installing
==========

Using PIP
---------

To install the latest released version of SAMS::

  $ pip install sams-server


Or to install a specific version of SAMS::

  $ pip install sams-server==0.2.3

From Source
-----------

You can download the source code for SAMS and install from that::

    $ git clone https://github.com/superdesk/sams.git
    $ cd sams/src/server
    $ pip install .



Minimal Config
==============

See :ref:`config` for a full reference to the available config attributes.

.. code-block:: python

   from sams.default_settings import env

   #: full mongodb connection uri
   MONGO_URI = env('SAMS_MONGO_URI', 'mongodb://localhost/sams')

   #: elastic url
   ELASTICSEARCH_URL = env('SAMS_ELASTICSEARCH_URL', 'http://localhost:9200')

   #: elastic index name
   ELASTICSEARCH_INDEX = env('SAMS_ELASTICSEARCH_INDEX', 'sams')

   #: Public URL used in `api` HATEOAS responses for downloading from the `file_server`
   SAMS_PUBLIC_URL = env('SAMS_PUBLIC_URL', 'http://localhost:5750')

   # Configure the StorageDestinations
   STORAGE_DESTINATION_1 = 'MongoGridFS,files,mongodb://localhost/sams_files'
   STORAGE_DESTINATION_2 = 'STORAGE_DESTINATION_2=AmazonS3,media,access=minioadmin,secret=minioadmin,region=minio,bucket=test,endpoint=http://localhost:9000'

.. warning::

  It is highly recommended to place Mongo, Elastic and StorageDestination configs into
  environment variables so your connection details are not exposed in a code repository.

.. note::

  Storage Destinations are, as the names states, a destination to store the binaries
  associated with an Asset.

  By default no Storage Destinations are configured. In order for the system to be usable
  you must define at least one Storage Destination.

  Config formats for the different Storage Providers

  * :mod:`sams.storage.providers.mongo`
  * :mod:`sams.storage.providers.amazon`
