import os

from api.settings import HOST, PORT, WORKERS, TIMEOUT

bind = '{}:{}'.format(HOST, PORT)
workers = WORKERS

accesslog = '-'
access_log_format = '%(m)s %(U)s status=%(s)s time=%(T)ss size=%(B)sb'

reload = 'SAMS_RELOAD' in os.environ

timeout = TIMEOUT
