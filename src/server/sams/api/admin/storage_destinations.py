from sams.factory.service import SamsService
from sams.storage.destinations import destinations
from superdesk.resource import Resource
from sams_client.schemas import destinationSchema
from superdesk.utils import ListCursor

class StorageDestinationsResource(Resource):
    """Resource instance for Storage Destinations
    """

    endpoint_name = 'destinations'
    url = 'admin/destinations'
    item_url = r'regex("[a-zA-Z0-9]+")'

    schema = destinationSchema

    item_methods = ['GET']
    resource_methods = ['GET']


class StorageDestinationsService(SamsService):
    """Service for storage destinations

    Returns one or all registered storage destinations
    """

    def get(self, req, **lookup):
        return ListCursor(list(map(
            lambda destination: destination.to_dict(),
            destinations.all().values()
        )))

    def find_one(self, req, **lookup):
        name = lookup['_id']
        destination = destinations.get(name)
        response = destination.to_dict()
        return response
