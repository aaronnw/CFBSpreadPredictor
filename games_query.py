import requests
import json
from global_config import years
from global_config import weeks
import os

PATH_JSON = 'data/game_results.json'

def query():
    if os.path.isfile(PATH_JSON) and os.access(PATH_JSON, os.R_OK):
        with open(PATH_JSON) as file:
            games = json.load(file)
            return games

    games = []
    for year in years:
        for week in weeks:
            headers = {
                'accept': 'application/json',
            }

            params = (
                ('year', str(year)),
                ('week', str(week)),
                ('seasonType', 'regular'),
            )

            response = requests.get('https://api.collegefootballdata.com/games', headers=headers, params=params)
            game = response.json()
            print(game)
            games.append(game)

    with open(PATH_JSON, 'w') as f:
        json.dump(games, f)

    return games
