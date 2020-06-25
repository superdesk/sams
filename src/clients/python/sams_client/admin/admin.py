from sams_client.client import SamsClient


class SamsClientAdmin(SamsClient):
    DESTINATIONS_API = '/admin/destinations/'

    def request_destination(self, id):
        return self.request(api=self.DESTINATIONS_API + id)

    def request_destinations(self):
        return self.request(api=self.DESTINATIONS_API)
