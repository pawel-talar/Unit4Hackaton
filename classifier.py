import nltk
import os
import random


texts_dir = 'scrapers/wikipedia'

features_count = 2000
featureset_size = 100
best_features_count = 10


def get_words_from_file(filepath):
    with open(filepath, 'r') as f:
        return f.read().split(' ')


def get_documents_data():
    categories = ['cs', 'economics', 'psychology', 'sport', 'linguistics']
    documents = []
    for category in categories:
        for f in os.listdir(os.path.join(texts_dir, category)):
            documents.append(
                (get_words_from_file(os.path.join(texts_dir, category, f)), category))
    return documents


def document_features(document, word_features):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in document_words)
    return features


def load_document(filepath):
    with open(filepath, 'r') as f:
        return f.read().split(' ')


if __name__ == '__main__':
    documents = get_documents_data()
    random.shuffle(documents)

    all_words = nltk.FreqDist(w.lower() for a in documents for w in a[0])
    word_features = list(all_words)[:features_count]

    # print(document_features(load_document('./cs/sql.txt'), word_features))
    featuresets = [(document_features(d, word_features), c) for (d,c) in documents]

    train_set, test_set = featuresets[featureset_size:], featuresets[:featureset_size]
    classifier = nltk.NaiveBayesClassifier.train(train_set)

    print(nltk.classify.accuracy(classifier, test_set))

    classifier.show_most_informative_features(best_features_count)
