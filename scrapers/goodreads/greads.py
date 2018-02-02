from goodreads import client
import json

def get_client():
    with open('../../config.json', 'r') as f:
        dict = json.load(f)

    client_id = dict['goodreads']['client_id']
    key = dict['goodreads']['key']

    gc = client.GoodreadsClient(client_id, key)
    gc.authenticate(client_id, key)

    return gc

def search_books(text_to_find):
    gc = get_client()
    books = gc.search_books(text_to_find, 1, 'all')
    return books[:10]

if __name__ == '__main__':
    print(search_books("Psychology"))