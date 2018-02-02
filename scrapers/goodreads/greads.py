from goodreads import client
import json

with open('../../config.json', 'r') as f:
    dict = json.load(f)
    f.close()

client_id = dict['goodreads']['client_id']
key = dict['goodreads']['key']

gc = client.GoodreadsClient(client_id, key)
gc.authenticate(client_id, key)

def search_books(text_to_find):
    books = gc.search_books(text_to_find, 1, 'all')
    return books[:10]