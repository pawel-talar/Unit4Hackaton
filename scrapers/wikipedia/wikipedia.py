import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import os.path
import logging
import json


config_path = os.path.abspath('../../config.json')
base_url = 'https://en.wikipedia.org/'


def cached():
    def cache(url):
        cache_filename = 'source_cache.txt'
        if os.path.exists(cache_filename):
            with open(cache_filename, 'r') as f:
                return f.read()
        source = f(url)
        with open('source_cache.txt', 'w') as f:
            f.write(source.decode())
    return cache


#@cached
def get_source(url):
    logging.debug("Getting source of {}".format(url))
    return urllib.request.urlopen(url).read()


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


def is_valid(word):
    min_length = 3
    return word.isalpha() and len(word) > min_length


def strip_word(word):
    characters_to_remove = ',.'
    for c in characters_to_remove:
        word = word.replace(c, '')
    return word


def clear_text(text):
    words = [strip_word(word).lower() for word in text.split(' ')]
    return ' '.join([word for word in words if is_valid(word)])


def get_article_text(source):
    bs = BeautifulSoup(source, 'html.parser')
    return ' '.join([clear_text(BeautifulSoup(a.text, "html.parser").text)
                   for a in bs.find_all('p')])


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
    logging.basicConfig(level=logging.DEBUG)
    for name, url in read_main_page_per_category(config_path).items():
        logging.info("Processing {} category".format(name))
        dirpath = os.path.abspath('./{}'.format(name))

        if not os.path.exists(dirpath):
            whole_body = save_texts(
                dirpath,
                get_category_texts(url))
            if len(whole_body) > 0:
                whole_category_filepath = dirpath + '.txt'
                with open(whole_category_filepath, 'w') as f:
                    logging.debug("Saving {} to {}".format(name, whole_category_filepath))
                    f.write(whole_body)
