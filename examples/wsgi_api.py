from sams.apps.api.app import get_app
from api import settings

application = get_app(__name__, config=settings)
