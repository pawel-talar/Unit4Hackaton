import random
import json
import logging

def request(category):
    logging.basicConfig(level=logging.DEBUG)

    config = open('config.json', 'r')
    output = open('./scrapers/openlearning/output.json')

    loaded_config = json.load(config)
    loaded_output = json.load(output)

    for each in range(5):
        topic = random.choice(loaded_config['categories-mapping']['courses'][category])
        data = random.choice(loaded_output['courses'])
        while(data['category'] != topic):
            data = random.choice(loaded_output['courses'])
            logging.info("Now selected course from {} category".format(data['category']))
        print(data['courseUrl'])

    config.close()
    output.close()