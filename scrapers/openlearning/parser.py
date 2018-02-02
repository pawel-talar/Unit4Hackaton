import json

with open('output.json') as json_data:
    data = json.load(json_data)
    json_data.close()

    f = open("openlearning_output","w+")

    for each in data['courses']:
        dictionary = {}
        dictionary['category'] = each['category']
        dictionary['url'] = each['courseUrl']
        dictionary['name'] = each['name']
        f.write(str(dictionary))
        f.write("\n")

f.close()
