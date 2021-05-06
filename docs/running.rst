=========================
Running SAMS Applications
=========================

There are currently two types of server side applications, the API and FileServer.

These applications can be started in a number of ways, depending on your needs:

* :ref:`CLI`
* :ref:`Honcho`
* :ref:`From Code`

CLI
---

This method uses the console to start the applications. This is generally used to test if SAMS was installed succesfully.

``API``
^^^^^^^

To start the API using the CLI::

  $ python -m sams.apps.api.wsgi

  ERROR:sams:file_path "logging_config.yml" not found
   * Serving Flask app "wsgi" (lazy loading)
   * Environment: production
     WARNING: This is a development server. Do not use it in a production deployment.
     Use a production WSGI server instead.
   * Debug mode: off
  INFO:werkzeug: * Running on http://localhost:5700/ (Press CTRL+C to quit)


``FileServer``
^^^^^^^^^^^^^^

To start the FileServer using the CLI::

  $ python -m sams.apps.file_server.wsgi

  ERROR:sams:file_path "logging_config.yml" not found
   * Serving Flask app "wsgi" (lazy loading)
   * Environment: production
     WARNING: This is a development server. Do not use it in a production deployment.
     Use a production WSGI server instead.
   * Debug mode: off
  INFO:werkzeug: * Running on http://localhost:5750/ (Press CTRL+C to quit)

Honcho
------

This method uses Honcho to start the applications. This is generally used for production purposes.

Procfile::

    api: gunicorn -c gunicorn_config_api.py sams.apps.api.wsgi
    file_server: gunicorn -c gunicorn_config_file_server.py sams.apps.file_server.wsgi


For example::

   cd src/server
   honcho start

   11:04:27 system        | api.1 started (pid=23228)
   11:04:27 system        | file_server.1 started (pid=23229)
   11:04:27 api.1         | [2020-10-30 11:04:27 +1100] [23228] [INFO] Starting gunicorn 20.0.4
   11:04:27 api.1         | [2020-10-30 11:04:27 +1100] [23228] [INFO] Listening at: http://0.0.0.0:5700 (23228)
   11:04:27 api.1         | [2020-10-30 11:04:27 +1100] [23228] [INFO] Using worker: sync
   11:04:27 file_server.1 | [2020-10-30 11:04:27 +1100] [23229] [INFO] Starting gunicorn 20.0.4
   11:04:27 api.1         | [2020-10-30 11:04:27 +1100] [23236] [INFO] Booting worker with pid: 23236
   11:04:27 file_server.1 | [2020-10-30 11:04:27 +1100] [23229] [INFO] Listening at: http://0.0.0.0:5750 (23229)
   11:04:27 file_server.1 | [2020-10-30 11:04:27 +1100] [23229] [INFO] Using worker: sync
   11:04:27 file_server.1 | [2020-10-30 11:04:27 +1100] [23237] [INFO] Booting worker with pid: 23237
   11:04:27 api.1         | 2020-10-30 11:04:27,924 level=DEBUG pid=23236 function=sams:logger:configure_logging Logging configured
   11:04:27 file_server.1 | 2020-10-30 11:04:27,926 level=DEBUG pid=23237 function=sams:logger:configure_logging Logging configured

From Code
---------

This method starts the application from your Python code. This is generally used to customise the application.

An example to start SAMS from code can be found in the examples folder https://github.com/superdesk/sams/tree/develop/examples

Custom API
^^^^^^^^^^

See :mod:`sams.apps.api` for further details about the API implementation

.. code-block:: python

   from sams.apps.api.app import get_app
   from sams.default_settings import env

   application = get_app(
       'SAMS_API',
       config=dict(
           SAMS_AUTH_TYPE: 'sams.auth.public'
       )
   )

   if __name__ == '__main__':
       application.run(
           host=application.config['HOST'],
           port=application.config['PORT'],
           debug=application.config['DEBUG'],
           use_reloader=application.config['DEBUG']
       )

Custom FileServer
^^^^^^^^^^^^^^^^^

See :mod:`sams.apps.file_server` for further details about the FileServer implementation

.. code-block:: python

   from sams.apps.file_server.app import get_app
   from sams.default_settings import env

   application = get_app(
       'SAMS_API',
       config=dict(
           SAMS_AUTH_TYPE: 'sams.auth.basic',
           CLIENT_API_KEYS: env('SAMS_PUBLIC_API_KEYS')
       )
   )

   if __name__ == '__main__':
       application.run(
           host=application.config['HOST'],
           port=application.config['PORT'],
           debug=application.config['DEBUG'],
           use_reloader=application.config['DEBUG']
       )
