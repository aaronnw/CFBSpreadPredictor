import requests
import json
from global_config import years
from global_config import weeks

data = []
for year in years:
    for week in weeks:
        headers = {
            'accept': 'application/json',
        }

        params = (
            ('year', str(year)),
            ('week', str(week)),
            ('seasonType', 'regular'),
            ('category', 'passing')
        )

        response = requests.get('https://api.collegefootballdata.com/games/players', headers=headers, params=params)
        game_objects = response.json()
        for game in game_objects:
            quarterbacks = game['teams'][0]['categories'][0]['types'][5]['athletes']
            print(quarterbacks)
        data.append(response.json())

with open('data.json', 'w') as f:
    json.dump(data, f)
