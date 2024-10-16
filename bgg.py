import xmltodict
import requests
import time

geeklist_id = '342440'
username = 'tofarley'
#geeklist_api = f'https://boardgamegeek.com/xmlapi/geeklist/{geeklist_id}'
geeklist_api = f'https://api.geekdo.com/api/listitems?listid={geeklist_id}'
geeklist_url = f'https://boardgamegeek.com/geeklist/{geeklist_id}'
usergames_url = f'https://boardgamegeek.com/xmlapi/collection/{username}&wanttoplay=1'


def get_games(url, time_limit):
    start_time = time.time()
    
    while True:
        r = requests.get(url)
        if r.status_code == 202:
            # Wait and try again later.
            time.sleep(1)
            # Check if the time limit has been exceeded
            if time.time() - start_time > time_limit:
                print("Time limit exceeded")
                return None
        else:
            break
    
    return xmltodict.parse(r.text)


r = requests.get(geeklist_api)

per_page = r.json()['pagination']['perPage']
total = r.json()['pagination']['total']
pages = total // per_page + 1

####
#pages = 1
####

available_games = []
for page in range(1, pages + 1):
#for page in range(17, 18):
    r = requests.get(f'{geeklist_api}&page={page}')
    for item in r.json()['data']:
        if 'sold' not in item['body'].lower():
            available_games.append(item)
            #import pdb; pdb.set_trace()
    time.sleep(0.2)

wishlist = get_games(usergames_url, 10)

matches = []

for wish in wishlist['items']['item']:
    for game in available_games:
        if game['item']['id'] == wish['@objectid']:
            matches.append(game)

for match in matches:
    # Future Tim, match['item'] has match['item']['imageid']
    print("%s: %s" % (match['item']['name'], "%s?itemid=%s" % (geeklist_url, match['id'])))

