import json
import os.path
import urllib.request
import scrapers.goodreads.greads as greads
import scrapers.openlearning.parser as olp
from flask import Flask
from flask import request


config_path = os.path.abspath('./config.json')


def get_classifier_address(config_path):
    with open(config_path, 'r') as f:
        classifier_data = json.loads(f.read())["classifier"]
        return classifier_data["host"], int(classifier_data["port"])


def get_page_category(classifier_host, classifier_port, page_url):
    request_url = "http://{}:{}?url={}".format(classifier_host,
                                               classifier_port, page_url)
    return urllib.request.urlopen(request_url).read().decode()


def get_book_for_category(category):
    return greads.search_books(category, 1, config_path)


def read_all_courses():
    path = './scrapers/openlearning/output.json'
    courses = None
    with open(path, 'r') as f:
        courses = json.loads(f.read())
    return courses


def map_courses_category(category):
    with open(config_path, 'r') as f:
        mappings = json.loads(f.read())["categories-mapping"]
        return mappings["courses"][category]


def get_courses_for_category(category):
    courses = read_all_courses()
    mapped_categories = map_courses_category(category)
    return [course for course in courses if course["category"] in mapped_categories]


if __name__ == '__main__':
    url = 'https://en.wikipedia.org/wiki/Central_processing_unit'
    host, port = get_classifier_address('./config.json')
    page_category = get_page_category(host, port, url)
    books = get_book_for_category(page_category)
    courses = get_courses_for_category(page_category)
