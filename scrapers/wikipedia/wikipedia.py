import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import os.path


base_url = 'https://en.wikipedia.org/'
category_main_page = 'https://en.wikipedia.org/wiki/Category:Top-Priority_mathematics_articles'


def get_source(url):
    cache_filename = 'source_cache.txt'
    if os.path.exists(cache_filename):
        with open(cache_filename, 'r') as f:
            return f.read()
    source = urllib.request.urlopen(url).read()
    with open('source_cache.txt', 'w') as f:
        f.write(source.decode())
    return urllib.request.urlopen(url).read()


def remove_talk_prefix(s):
    return s.replace('Talk:', '')


def get_article_url(base, href):
    return urllib.parse.urljoin(base, remove_talk_prefix(href))


def is_article_url(url):
    return not ('Top-Priority' in url or '#' in url)


def get_articles_urls(source):
    bs = BeautifulSoup(source, 'html.parser')
    elements = bs.find(class_='mw-category-generated').find_all('a')
    urls = [get_article_url(base_url, article_elem.get('href'))
            for article_elem in elements]
    return [url for url in urls if is_article_url(url)]


if __name__ == '__main__':
    src = get_source(category_main_page)
    urls = get_articles_urls(src)
    print(urls)
