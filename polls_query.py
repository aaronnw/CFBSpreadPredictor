import requests
import json
from global_config import years
from global_config import weeks
import os

PATH_AP_JSON = 'data/ap_poll.json'
PATH_COACHES_JSON = 'data/coaches_poll.json'

def query():
    if os.path.isfile(PATH_AP_JSON) and os.access(PATH_AP_JSON, os.R_OK) and os.path.isfile(PATH_COACHES_JSON) and os.access(PATH_COACHES_JSON, os.R_OK) :
        with open(PATH_AP_JSON) as file:
            ap_polls = json.load(file)
        with open(PATH_COACHES_JSON) as file:
            coaches_polls = json.load(file)
        return ap_polls, coaches_polls

    ap_polls = {}
    coaches_polls = {}
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
            ap_poll_query = response.json()['rankings'][0]['ranks']
            ap_poll = {}
            for pos in ap_poll_query:
                team_name = pos['team']['nickname']
                rank = pos['current']
                ap_poll[team_name] = rank

            coaches_poll_query = response.json()['rankings'][1]['ranks']
            coaches_poll = {}
            for pos in coaches_poll_query:
                team_name = pos['team']['nickname']
                rank = pos['current']
                coaches_poll[team_name] = rank

            ap_polls[str(year) + "," + str(week)] = ap_poll
            coaches_polls[str(year) + "," + str(week)] = coaches_poll

    with open(PATH_AP_JSON, 'w') as f:
        json.dump(ap_polls, f)

    with open(PATH_COACHES_JSON, 'w') as f:
        json.dump(coaches_polls, f)

    return ap_polls, coaches_polls