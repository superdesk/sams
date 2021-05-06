import multiprocessing
from os import path
from pathlib import Path

from sams.default_settings import env

ABS_PATH = str(Path(__file__).resolve().parent)

#: hostname the FileServer runs on
HOST = env('SAMS_PUBLIC_HOST', '0.0.0.0')

#: port the FileServer runs on
PORT = int(env('SAMS_PUBLIC_PORT', '5750'))

#: full url for the FileServer
SERVER_URL = env('SAMS_API_URL', f'http://{HOST}:{PORT}')

#: Gunicorn workers/timeout
WORKERS = int(env('SAMS_PUBLIC_WORKERS', env('WEB_CONCURRENCY', multiprocessing.cpu_count() + 1)))
TIMEOUT = int(env('SAMS_PUBLIC_TIMEOUT', env('WEB_TIMEOUT', 30)))

#: Type of authentication to use
SAMS_AUTH_TYPE = 'sams.auth.basic'
CLIENT_API_KEYS = env('SAMS_PUBLIC_API_KEYS')  # Comma separated list of API Keys

#: Location of the log file
LOG_CONFIG_FILE = path.join(ABS_PATH, 'logging_config.yml')
