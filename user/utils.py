import requests


class RestAPI:

    def __init__(self):
        self.url = "http://localhost:8080/shoppingmall"
        self.headers = {
            'content-type': "application/json"
        }

    def api_get(self, url, param):
        destination = self.url + url
        response = requests.get(destination, params=param)
        return response.text


