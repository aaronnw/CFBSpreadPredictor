import requests
import json
from global_config import years
from global_config import weeks
import os

PATH_AP_JSON = 'data/ap_poll.json'
PATH_COACHES_JSON = 'data/coaches_poll.json'

def query():
    if os.path.isfile(PATH_AP_JSON) and os.access(PATH_AP_JSON, os.R_OK) and os.path.isfile(PATH_COACHES_JSON) and os.access(PATH_COACHES_JSON, os.R_OK) :
        ap_polls = json.loads(PATH_AP_JSON)
        coaches_polls = json.loads(PATH_AP_JSON)
        return ap_polls, coaches_polls

    ap_polls = []
    coaches_polls = []
    for year in years:
        for week in weeks:
            headers = {
                'accept': 'application/json',
            }

            params = (
                ('seasons', str(year)),
                ('weeks', str(week))
            )

            response = requests.get('http://site.api.espn.com/apis/site/v2/sports/football/college-football/rankings', headers=headers, params=params)
            ap_poll = response.json()['rankings'][0]['ranks']
            coaches_poll = response.json()['rankings'][1]['ranks']
            ap_polls.append(ap_poll)
            coaches_polls.append(coaches_poll)

    with open(PATH_AP_JSON, 'w') as f:
        json.dump(ap_polls, f)

    with open(PATH_COACHES_JSON, 'w') as f:
        json.dump(coaches_polls, f)
