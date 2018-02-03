import nltk
import os
import random
import logging
from scrapers.utils import *
from flask import Flask
from flask import request


texts_dir = 'scrapers/wikipedia'

features_count = 10000
featureset_size = 200
best_features_count = 10
max_words = 200000


def get_words_from_file(filepath):
    with open(filepath, 'r') as f:
        words = f.read().split(' ')
        random.shuffle(words)
        return words[:max_words]


def get_documents_data():
    categories = ['cs', 'sport', 'psychology', 'linguistics', 'mathematics']
    documents = []
    for category in categories:
        for f in os.listdir(os.path.join(texts_dir, category)):
            documents.append(
                (get_words_from_file(os.path.join(texts_dir, category, f)), category))
    return documents


def document_features(document, word_features):
    logging.debug(document)
    document_words = set(document)
    logging.debug(document_words)
    features = {}
    for word in word_features:
        features[word] = (word in document_words)
    return features


def load_document(filepath):
    with open(filepath, 'r') as f:
        return f.read().split(' ')


def get_trained_classifier(documents, word_features):
    global classifier
    featuresets = [(document_features(d, word_features), c) for (d,c) in documents]
    logging.debug("featuresets size: {}".format(len(featuresets)))

    train_set, test_set = featuresets[featureset_size:], featuresets[:featureset_size]
    classifier = nltk.DecisionTreeClassifier.train(train_set)

    logging.info("Classifier accuracy: {}".format(
        nltk.classify.accuracy(classifier, test_set)))

    return classifier


def classify_web_page(classifier, url, word_features):
    logging.debug("running classification for {}".format(url))
    source = get_source(url)
    cleared_text = clear_text(get_article_text(source))
    class_ = classifier.classify(document_features(cleared_text.split(' '),
                                                   word_features))
    logging.debug("got class: {}".format(class_))
    return class_


word_features = None
classifier = None
app = Flask(__name__)


@app.before_first_request
def init_classifier():
    global word_features
    global classifier
    logging.basicConfig(level=logging.INFO)
    documents = get_documents_data()
    random.shuffle(documents)

    all_words = nltk.FreqDist(w.lower() for a in documents for w in a[0])
    logging.debug("all_words size: {}".format(len(all_words)))
    word_features = list(all_words)[:features_count]

    classifier = get_trained_classifier(documents, word_features)


@app.route('/', methods=['GET'])
def index():
    url = request.args.get('url')
    if classifier is None or word_features is None:
        return 'None'
    return classify_web_page(classifier, url, word_features)


