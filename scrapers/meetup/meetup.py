import json
import urllib.parse
import requests

api_url = 'https://api.meetup.com'
code = 'cbd72b775052fe51c3d08cd337116b45'
key = '1ultt2ilhvtsegdif4p299ohpf'
secret = 'b6iqrru5ontmh9utj9msu3bnkk'
redirect_uri = 'https://github.com'

def status():
    r = requests.get(api_url + '/status')
    return r.status_code, r.text


def get_groups(token):
    url = 'https://api.meetup.com/find/groups?zip=11321&radius=1&category=,&upcoming_events=true&order=members'
    headers = {"Authorization": "Bearer {}".format(token)}
    r = requests.get(url, headers=headers)
    d = r.text
    table_of_names = json.loads(d)
    return table_of_names

def get_categories(token):
    url = 'https://api.meetup.com//find/topic_categories?zip=11211&'
    headers = {"Authorization": "Bearer {}".format(token)}
    r = requests.get(url, headers=headers)
    d = r.text
    table_of_names = json.loads(d)
    return table_of_names

def get_token(code):
    url = 'https://secure.meetup.com/oauth2/access'
    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
    payload = {
        'client_id': key,
        'client_secret': secret,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri,
        'code': code
    }
    print(payload)
    r = requests.post(url, data=urllib.parse.urlencode(payload), headers=headers)
    return r.status_code, r.text


if __name__ == '__main__':  
    token = '0627f2b21779b335558ca93737cb62a5'
    categories = get_categories(token)
    groups = get_groups(token)
    file = open('data.txt', 'w')
    size = len(groups)
    l = 0
    for i in range(size):
        x = groups[i]['name']
        y = groups[i]['category']['id']
        if y >= 0 and y <= 23:    
            file.write(categories[y]['name']+" -- ")
        file.write(str(x)+'\n')
    
    file.closed