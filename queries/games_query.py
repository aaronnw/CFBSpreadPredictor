import requests
import json
from global_config import years
from global_config import test_year
from global_config import weeks
from global_config import file_access


GAME_RESULTS_PATH = 'data/game_results.json'
TEST_GAMES_PATH = 'data/test_games.json'


def query():
    if file_access(GAME_RESULTS_PATH) and file_access(TEST_GAMES_PATH):
        with open(GAME_RESULTS_PATH) as file:
            games = json.load(file)
        with open(TEST_GAMES_PATH) as file:
            test_games = json.load(file)
        return games, test_games

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

    test_games = []
    if test_year != 0:
        for week in weeks:
            headers = {
                'accept': 'application/json',
            }

            params = (
                ('year', str(test_year)),
                ('week', str(week)),
                ('seasonType', 'regular'),
            )

            response = requests.get('https://api.collegefootballdata.com/games', headers=headers, params=params)
            game = response.json()
            test_games.append(game)

        with open(TEST_GAMES_PATH, 'w') as f:
            json.dump(test_games, f)

    with open(GAME_RESULTS_PATH, 'w') as f:
        json.dump(games, f)

    return games, test_games
