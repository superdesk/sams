.. _settings:

.. module:: sams.default_settings

=============
Configuration
=============

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

Default: ``[]``

You can install additional modules by adding their names here.

Mongo connections
-----------------

``HOST``
^^^^^^^^

Default: ``'0.0.0.0'``

``PORT``
^^^^^^^^

Default: ``'5700'``

``MONGO_DBNAME``
^^^^^^^^^^^^^^^^

Default: ``'sams'``

``MONGO_URI``
^^^^^^^^^^^^^

Default: ``'mongodb://localhost/sams'``

Elastic settings
----------------

``ELASTICSEARCH_URL``
^^^^^^^^^^^^^^^^^^^^^

Default: ``'http://localhost:9200'``

``ELASTICSEARCH_INDEX``
^^^^^^^^^^^^^^^^^^^^^^^

Default: ``'sams'``

Monitoring settings
-------------------

``SENTRY_DSN``
^^^^^^^^^^^^^^

Default: ``None``

Storage Provider/Destination settings
-------------------------------------
``STORAGE_PROVIDERS``
^^^^^^^^^^^^^^^^^^^^^

Default::

    [
        'sams.storage.providers.mongo.MongoGridFSProvider',
        'sams.storage.providers.amazon.AmazonS3Provider',
    ]

``STORAGE_DESTINATION_<x>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Default: ``None``

Asset settings
--------------

``MAX_ASSET_SIZE``
^^^^^^^^^^^^^^^^^^

Default: ``0``

Set's a global restriction on the maximum size of an Asset allowed to be uploaded.
