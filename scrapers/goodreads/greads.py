from goodreads import client
import json

path = '../../config.json'

def get_client():
    with open(path, 'r') as f:
        dict = json.load(f)

    client_id = dict['services']['goodreads']['client_id']
    key = dict['services']['goodreads']['key']

    gc = client.GoodreadsClient(client_id, key)
    gc.authenticate(client_id, key)

    return gc

def search_books(category, n):
    with open(path, 'r') as f:
        dict = json.load(f)['services']['goodreads']
    return dict[category][:n]

if __name__ == '__main__':
    with open(path, 'r') as f:
        dict = json.load(f)['services']['goodreads']