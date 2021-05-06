import superdesk
from flask_script import Manager
from sams.apps.api.app import get_app
from api import settings

application = get_app(__name__, config=settings)
manager = Manager(application)

if __name__ == '__main__':
    with application.app_context():
        manager.run(superdesk.COMMANDS)
