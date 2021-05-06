from sams.apps.api.app import get_app
from api import settings

application = get_app(__name__, config=settings)

if __name__ == '__main__':
    application.run(
        host=application.config['HOST'],
        port=application.config['PORT'],
        debug=application.config['DEBUG'],
        use_reloader=application.config['DEBUG']
    )
