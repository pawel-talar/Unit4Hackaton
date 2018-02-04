from bs4 import BeautifulSoup
import logging
import urllib.request


def get_source(url):
    logging.debug("Getting source of {}".format(url))
    return urllib.request.urlopen(url).read()


def is_valid(word):
    min_length = 3
    forbidden = ['there', 'have', 'with', 'that', 'which', 'this', 'than',
                 'from', 'such', 'when', 'these']
    return len(word) > min_length and (word not in forbidden and word.isalpha())


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
