
import os
import multiprocessing

bind = '{}:{}'.format(
    os.environ.get('SAMS_HOST', '0.0.0.0'),
    os.environ.get('SAMS_PORT', '5700')
)
workers = int(os.environ.get('WEB_CONCURRENCY', multiprocessing.cpu_count() + 1))

accesslog = '-'
access_log_format = '%(m)s %(U)s status=%(s)s time=%(T)ss size=%(B)sb'

reload = 'SAMS_RELOAD' in os.environ

timeout = int(os.environ.get('WEB_TIMEOUT', 30))
