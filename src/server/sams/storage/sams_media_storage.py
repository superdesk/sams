from eve.io.media import MediaStorage
from flask import g
from uuid import uuid4


def get_request_id():
    """
    Returns request id for media cache
    """
    if not getattr(g, 'request_id', None):
        g.request_id = uuid4()
    return g.request_id


class SamsMediaStorage(MediaStorage):
    cache = {}

    def get(self, _id, resource=None):
        pass

    def delete(self, id_or_filename, resource=None):
        pass

    def put(self, content, **kwargs):
        """
        Uploads binary while creating or updating asset
        """
        request_id = get_request_id()
        # store binary in cache
        self.cache[request_id] = content
