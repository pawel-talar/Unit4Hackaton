import logging
import time
from os.path import expanduser
import unit4_hackaton.history_gatherer as hg
import requests

profile_name = 'mxhml4y1.default'
history_path = expanduser("~") + '/.mozilla/firefox/' + profile_name + \
               '/places.sqlite'


def main():
    logging.basicConfig(level=logging.DEBUG)
    history_gatherer = hg.HistoryGatherer(history_path)
    delay = 2
    while True:
        time.sleep(delay)
        urls = [url for url in history_gatherer.get_urls() if 'wikipedia' in url]
        for url in urls:
            ru = 'http://localhost:5001/submit'
            headers = {"Content-Type": "text/plain"}
            logging.info("ru: {} data: {} headers: {}".format(ru, url, headers))
            try:
                r = requests.post(ru, data=url, headers=headers)
                if r.status_code == 200:
                    history_gatherer.cache(url)
            except requests.ConnectionError as e:
                logging.error(
                    "Assistant service not available: {}".format(str(e)))


if __name__ == '__main__':
    main()
