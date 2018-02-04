import urllib.parse
import requests


class AssistantUnreachable(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class AssistantClient:
    submit_method_name = "submit"
    submit_headers = {"Content-Type": "text/plain"}

    def __init__(self, address):
        assert type(address["port"] == int)
        self.base_url = "{}:{}".format(address["host"], address["port"])
        self.submit_url = urllib.parse.urljoin(
            self.base_url, self.submit_method_name
        )

    def submit(self, url):
        try:
            r = requests.post(self.submit_url, data=url,
                              headers=self.submit_headers)
            if r.status_code != 200:
                raise AssistantUnreachable("Cannot connect to assistant "
                                           "service")
        except requests.ConnectionError as e:
            raise AssistantUnreachable(str(e))
