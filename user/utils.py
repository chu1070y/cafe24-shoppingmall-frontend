import requests


class RestAPI:

    def __init__(self):
        self.url = "http://localhost:8080/shoppingmall"
        self.headers = {
            'content-type': "application/json"
        }

    def api_get(self, url, param=""):
        destination = self.url + url
        response = requests.get(destination, params=param)
        return response.text

    def api_post(self, url, data=""):
        destination = self.url + url
        response = requests.post(destination, data=data, headers=self.headers)
        return response.text


