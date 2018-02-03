import json
import os.path
import logging
import urllib.request
from flask import Flask
from flask import request
from flask import render_template
import redis

import scrapers.goodreads.greads
import courses_handler
import meetup_handler

config_path = os.path.abspath('./config.json')
logging.basicConfig(level=logging.DEBUG)

books_key = 'books'
meetups_key = 'meetups'
courses_key = 'courses'


def get_classifier_address(config_path):
    with open(config_path, 'r') as f:
        classifier_data = json.loads(f.read())["classifier"]
        return classifier_data["host"], int(classifier_data["port"])


def get_page_category(classifier_host, classifier_port, page_url):
    request_url = "http://{}:{}?url={}".format(classifier_host,
                                               classifier_port, page_url)
    return urllib.request.urlopen(request_url).read().decode()


def get_book_for_category(category):
    return scrapers.goodreads.greads.search_books(category, 1, config_path)


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
    logging.debug("Courses: {}".format(courses))
    mapped_categories = map_courses_category(category)
    return courses_handler.request(category)


r = None

app = Flask(__name__)


@app.before_first_request
def initialize():
    global r
    with open(config_path, 'r') as f:
        redis_data = json.loads(f.read())["redis"]
        r = redis.StrictRedis(host=redis_data["host"], port=redis_data["port"],
                              db=0)


@app.route('/', methods=['GET'])
def status():
    books = [x.decode() for x in set(r.lrange(books_key, 0, 5))]
    courses = [json.loads(x) for x in set(r.lrange(courses_key, 0, 5))]
    meetups = [json.loads(x) for x in set(r.lrange(meetups_key, 0, 5))]
    logging.debug(books)
    logging.debug(courses)
    logging.debug(meetups)

    return render_template('status.html', books=books, courses=courses,
                           meetups=meetups)


@app.route('/submit', methods=['POST'])
def submit_url():
    url = request.data.decode()
    host, port = get_classifier_address('./config.json')
    page_category = get_page_category(host, port, url)
    book = get_book_for_category(page_category)[0]
    course = get_courses_for_category(page_category)[0]
    meetup = list(meetup_handler.handler(page_category))[0]
    logging.debug("Book: {}".format(book))
    logging.debug("Course: {}".format(course))
    logging.debug("Meetup: {}".format(meetup))
    r.lpush(books_key, book)
    r.lpush(courses_key, json.dumps(course))
    r.lpush(meetups_key, json.dumps(meetup))
    return "url submitted", 200
