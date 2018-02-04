import sqlite3
import os.path
import logging
import time
from os.path import expanduser
import requests

profile_name = 'mxhml4y1.default'
history_path = expanduser("~") + '/.mozilla/firefox/' + profile_name + \
               '/places.sqlite'


def connect_to_sqlite(db_path):
    conn = sqlite3.connect(db_path)
    return conn


already_visited = set()


def get_urls(conn):
    global already_visited
    query_str = """
SELECT p.url FROM moz_historyvisits AS h, moz_places AS p
WHERE p.id == h.place_id
ORDER BY h.visit_date"""

    c = conn.cursor()
    urls = set([row[0] for row in c.execute(query_str)])
    to_return = urls - already_visited
    return list(to_return)


def main():
    delay = 2
    logging.basicConfig(level=logging.DEBUG)
    print(history_path)
    conn = connect_to_sqlite(history_path)
    while True:
        time.sleep(delay)
        urls = [url for url in get_urls(conn) if 'wikipedia' in url]
        for url in urls:
            ru = 'http://localhost:5001/submit'
            headers = {"Content-Type": "text/plain"}
            logging.info("ru: {} data: {} headers: {}".format(ru, url, headers))
            try:
                r = requests.post(ru, data=url, headers=headers)
                already_visited = already_visited | set([url])
            except requests.ConnectionError as e:
                logging.error(
                    "Assistant service not available: {}".format(str(e)))


if __name__ == '__main__':
    main()
