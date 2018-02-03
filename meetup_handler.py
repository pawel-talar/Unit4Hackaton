import json
import random

def handler(category):
    config = open('config.json')
    data = open('./scrapers/meetup/events.json')
    groups = open('./scrapers/meetup/groups-formatted.json')

    loaded_config = json.load(config)
    loaded_data = json.load(data)
    loaded_groups = json.load(groups)

    topic_number = loaded_config['meetup'][category][0]
    #print(topic_number)
    for every in range(5):
        str = "next_event"
        group_id = random.choice(loaded_groups)
        while((group_id['category']['id'] != topic_number) or (str not in group_id)):
            group_id = random.choice(loaded_groups)


        event_id = group_id['next_event']['id']
        for each in loaded_data['events']:
            if each['id'] == event_id:
                print(each['name'],"\n", each['link'],"\n\n")


    config.close()
    data.close()



