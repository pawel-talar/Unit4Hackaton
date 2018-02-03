import json
import logging

with open('output.json') as json_data:
    data = json.load(json_data)
    json_data.close()

    logging.basicConfig(level=logging.DEBUG)
    f = open("openlearning_output","w+")

    for each in data['courses']:
        dictionary = {}
        dictionary['category'] = each['category']
        dictionary['url'] = each['courseUrl']
        dictionary['name'] = each['name']
        logging.info("Saving course from {}".format(each['courseUrl']))
        f.write(str(dictionary))
        f.write("\n")

f.close()