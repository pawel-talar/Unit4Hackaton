from goodreads import client
import json

path = '../../config.json'

def get_client():
    with open(path, 'r') as f:
        dict = json.load(f)

    client_id = dict['goodreads']['client_id']
    key = dict['goodreads']['key']

    gc = client.GoodreadsClient(client_id, key)
    gc.authenticate(client_id, key)

    return gc

def search_books(text_to_find, n):
    gc = get_client()
    books = gc.search_books(text_to_find, 1, 'all')
    return books[:5]

if __name__ == '__main__':
    with open(path, 'r') as f:
        dict = json.load(f)['goodreads']
    print(search_books(dict['mathematics'], 5))
    print(search_books(dict['cs'], 5))
    print(search_books(dict['economics'], 5))
    print(search_books(dict['psychology'], 5))
    print(search_books(dict['sport'], 5))