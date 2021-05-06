.. _settings:

.. module:: sams.default_settings

======
Config
======

We use ``flask.app.config``, so to use it do::

    from flask import current_app as app

    print(app.config['SERVER_DOMAIN'])

Configuration is combination of default settings module and settings module
in `application repo <https://github.com/superdesk/sams/blob/master/server/default_settings.py>`_.

.. _settings.default:

Default settings
----------------

``INSTALLED_APPS``
^^^^^^^^^^^^^^^^^^

**Default**: ``[]``

You can install additional modules by adding their names here.

Mongo connections
-----------------

``HOST``
^^^^^^^^

**Default**: ``'localhost'``

**Env. Var [API]**: ``SAMS_HOST``

**Env. Var [FileServer]**: ``SAMS_PUBLIC_HOST``

``PORT``
^^^^^^^^

**Default [API]**: ``'5700'``

**Default [FileServer]**: ``'5750'``

**Env. Var [API]**: ``SAMS_PORT``

**Env. Var [FileServer]**: ``SAMS_PUBLIC_PORT``

``MONGO_DBNAME``
^^^^^^^^^^^^^^^^

**Default**: ``'sams'``

**Env. Var**: ``SAMS_MONGO_DBNAME``

``MONGO_URI``
^^^^^^^^^^^^^

**Default**: ``'mongodb://localhost/sams'``

**Env. Var**: ``SAMS_MONGO_URI``

Elastic settings
----------------

``ELASTICSEARCH_URL``
^^^^^^^^^^^^^^^^^^^^^

**Default**: ``'http://localhost:9200'``

**Env. Var**: ``SAMS_ELASTICSEARCH_URL``

``ELASTICSEARCH_INDEX``
^^^^^^^^^^^^^^^^^^^^^^^

**Default**: ``'sams'``

**Env. Var**: ``SAMS_ELASTICSEARCH_INDEX``

Monitoring settings
-------------------

``SENTRY_DSN``
^^^^^^^^^^^^^^

**Default**: ``None``

**Env. Var**: ``SAMS_SENTRY_DSN``

``LOG_CONFIG_FILE``
^^^^^^^^^^^^^^^^^^^

**Default**: ``logging_config.yml`` (in the current working directory)

**Env. Var [API]**: ``SAMS_LOG_CONFIG``

**Env. Var [FileServer]**: ``SAMS_PUBLIC_LOG_CONFIG``

Storage Provider/Destination settings
-------------------------------------
``STORAGE_PROVIDERS``
^^^^^^^^^^^^^^^^^^^^^

**Default**::

    [
        'sams.storage.providers.mongo.MongoGridFSProvider',
        'sams.storage.providers.amazon.AmazonS3Provider',
    ]

``STORAGE_DESTINATION_<x>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Default**: ``None``

Asset settings
--------------

``MAX_ASSET_SIZE``
^^^^^^^^^^^^^^^^^^

**Default**: ``'0'``

**Env. Var**: ``SAMS_MAX_ASSET_SIZE``

Set's a global restriction on the maximum size of an Asset allowed to be uploaded.

Authentication
--------------

Use the following config attribute to control the type of authentication the application will use.
This variable will point to the Python module to use.

``SAMS_AUTH_TYPE``
^^^^^^^^^^^^^^^^^^

**Default**: ``'sams.auth.public'``

**Env. Var [API]**: ``SAMS_AUTH_TYPE``

**Env. Var [FileServer]**: ``SAMS_PUBLIC_AUTH_TYPE``

In-built authentication modules:

* ``sams.auth.public`` (No Authentication)
* ``sams.auth.basic`` (Basic HTTP Authentication)

``CLIENT_API_KEYS``
^^^^^^^^^^^^^^^^^^^

This config attribute is for use by ``sams.auth.basic`` module, and will provide the API Keys to allow.

The value should be a comma separated list of API Keys.

**Default**: ``''``

**Env. Var [API]**: ``SAMS_CLIENT_API_KEYS``

**Env. Var [FileServer]**: ``SAMS_PUBLIC_API_KEYS``
