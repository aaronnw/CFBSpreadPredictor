import requests
import os
from global_config import years
from global_config import test_year
from global_config import weeks
from utils import file_access, save_json, load_json

GAME_RESULTS_PATH = 'data/game_results.json'
TEST_GAMES_PATH = 'data/test_games.json'


def query():
    if file_access(GAME_RESULTS_PATH) and file_access(TEST_GAMES_PATH):
        return load_json(GAME_RESULTS_PATH), load_json(TEST_GAMES_PATH)

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

    save_json(test_games, TEST_GAMES_PATH)
    save_json(games, GAME_RESULTS_PATH)

    return games, test_games
