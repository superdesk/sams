from sams.factory.service import SamsService
from sams.storage.destinations import destinations
from superdesk.resource import Resource
from sams_client.schemas import destinationSchema


class StorageDestinationsResource(Resource):
    """
    **schema** =
        ``name`` *string*
            Destination name
        ``provider` *string*
            Destination's Provider name
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

    def find(self, req, **lookup):
        return list(map(
            lambda destination: destination.to_dict(),
            destinations.all().values()
        ))

    def find_one(self, req, **lookup):
        name = lookup['_id']
        destination = destinations.get(name)
        response = destination.to_dict()
        return response
