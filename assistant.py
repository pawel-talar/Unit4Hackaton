import json
import urllib.request


def get_classifier_address(config_path):
    with open(config_path, 'r') as f:
        classifier_data = json.loads(f.read())["classifier"]
        return classifier_data["host"], int(classifier_data["port"])


def get_page_category(classifier_host, classifier_port, page_url):
    request_url = "http://{}:{}?url={}".format(classifier_host,
                                               classifier_port, page_url)
    return urllib.request.urlopen(request_url).read().decode()


if __name__ == '__main__':
    url = 'https://en.wikipedia.org/wiki/Central_processing_unit'
    host, port = get_classifier_address('./config.json')
    category = get_page_category(host, port, url)
