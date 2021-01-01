import requests
from global_config import years
from global_config import weeks
from utils import file_access, save_json, load_json

GAME_RESULTS_PATH = 'data/game_results.json'


def query():
    if file_access(GAME_RESULTS_PATH):
        return load_json(GAME_RESULTS_PATH)

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
            games.append(game)

    save_json(games, GAME_RESULTS_PATH)

    return games
