import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import os.path
import logging
import json
from scrapers.utils import *


config_path = os.path.abspath('../../config.json')
base_url = 'https://en.wikipedia.org/'


def remove_talk_prefix(s):
    return s.replace('Talk:', '')


def get_article_url(base, href):
    return urllib.parse.urljoin(base, remove_talk_prefix(href))


def is_article_url(url):
    return not ('Top-Priority' in url or '#' in url)


def get_articles_urls(source):
    logging.debug("Getting articles urls")
    bs = BeautifulSoup(source, 'html.parser')
    elements = bs.find(class_='mw-category-generated').find_all('a')
    urls = (get_article_url(base_url, article_elem.get('href'))
            for article_elem in elements)
    return (url for url in urls if is_article_url(url))


def parse_text_from_url(url):
    logging.debug("Parsing text from {}".format(url))
    return get_article_text(get_source(url))


def convert_category_url_to_name(url):
    basename = urllib.parse.urlparse(url).path.split('/')[-1]
    return basename.lower().replace('(', '').replace(')', '')


def get_category_texts(category_url):
    src = get_source(category_url)
    urls = get_articles_urls(src)
    for url in urls:
        yield (convert_category_url_to_name(url), parse_text_from_url(url))


def save_texts(dirpath, texts):
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    whole_body = ''
    for name, body in texts:
        whole_body = whole_body + ' ' + body
        filepath = os.path.join(dirpath, "{}.txt".format(name))
        with open(filepath, 'w') as f:
            logging.debug("Saving {} to {}".format(name, filepath))
            f.write(body)
    return whole_body


def read_main_page_per_category(config_path):
    with open(config_path, 'r') as f:
        return json.loads(f.read())["services"]["wikipedia-urls"]


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    for name, urls in read_main_page_per_category(config_path).items():
        for url in urls:
            logging.info("Processing {} category".format(name))
            dirpath = os.path.abspath('./{}'.format(name))

            whole_body = save_texts(
                dirpath,
                get_category_texts(url))
            if len(whole_body) > 0:
                whole_category_filepath = dirpath + '.txt'
                with open(whole_category_filepath, 'w') as f:
                    logging.debug("Saving {} to {}".format(name, whole_category_filepath))
                    f.write(whole_body)
