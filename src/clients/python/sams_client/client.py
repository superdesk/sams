import requests
from .utils import get_base_url


class Client(object):
    def __init__(self, configs={}):
        self.base_url = get_base_url(configs)

    def request(self, api='/', method='get',
                headers=None, data=None, callback=None):
        if callback is None:
            callback = self._default_resp_callback
        request = getattr(requests, method.lower())
        url = f'{self.base_url}{api}'
        response = request(url, headers=headers, data=data)
        response.raise_for_status()
        return callback(response)

    def _default_resp_callback(self, response):
        return response
