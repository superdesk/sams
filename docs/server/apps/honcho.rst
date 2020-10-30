Starting Apps with Honcho
=========================

There is a Procfile located at ``src/server/Procfile`` and can be started using ``honcho``

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

