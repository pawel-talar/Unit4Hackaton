import random
import json
import logging


def request(category, n=1):
    logging.basicConfig(level=logging.DEBUG)

    config = open('config.json', 'r')
    output = open('./scrapers/openlearning/output.json')

    loaded_config = json.load(config)
    loaded_output = json.load(output)

    courses = []

    for each in range(n):
        topic = random.choice(loaded_config['categories-mapping']['courses'][category])
        data = random.choice(loaded_output['courses'])
        while(data['category'] != topic):
            data = random.choice(loaded_output['courses'])
            logging.info("Now selected course from {} category".format(data['category']))
        courses.append({'name': data['name'], 'url': data['courseUrl']})

    config.close()
    output.close()

    return courses
