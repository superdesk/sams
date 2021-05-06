import multiprocessing
from os import path
from pathlib import Path

from sams.default_settings import env

ABS_PATH = str(Path(__file__).resolve().parent)

#: hostname the API runs on
HOST = env('SAMS_API_HOST', 'localhost')

#: port the API runs on
PORT = int(env('SAMS_API_PORT', '5700'))

#: full url for this API
SERVER_URL = env('SAMS_API_URL', f'http://{HOST}:{PORT}')

#: Gunicorn workers/timeout
WORKERS = int(env('SAMS_API_WORKERS', env('WEB_CONCURRENCY', multiprocessing.cpu_count() + 1)))
TIMEOUT = int(env('SAMS_API_TIMEOUT', env('WEB_TIMEOUT', 30)))

#: Type of authentication to use
SAMS_AUTH_TYPE = 'sams.auth.public'

#: Location of the log file
LOG_CONFIG_FILE = path.join(ABS_PATH, 'logging_config.yml')

#: Maximum upload size of an Asset
MAX_ASSET_SIZE = int(env('SAMS_MAX_ASSET_SIZE', '0'))
