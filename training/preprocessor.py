import json
import os
from collections import defaultdict

import jsonpickle as jsonpickle
import numpy as np

from game_data import Game
from utils import file_access
from training import data_collector
from global_config import GAME_DATA_PATH, TEST_GAME_DATA_PATH
from training.queries import games_query


def split_datasets(all_data, pct_val, pct_test):
    np.random.shuffle(all_data)

    # Number of samples in each set
    testing_num = int(pct_test * len(all_data))
    validation_num = int(pct_val*len(all_data))
    training_num = len(all_data)-1-testing_num-validation_num

    training_data = all_data[0:training_num]
    validation_data = all_data[training_num:training_num + validation_num]
    testing_data = all_data[training_num + validation_num:]

    return training_data, validation_data, testing_data


def create_netdata_from_gamedata(gamedata):
    all_inputs = []
    all_outputs = [game.output for game in gamedata]
    # all_inputs = [tuple(game.inputs.values()) for game in gamedata]
    stats_to_use = ["average-scoring-margin", "red-zone-scoring-pct", "third-down-conversion-pct", "yards-per-play", "average-team-passer-rating", "yards-per-rush-attempt", "turnover-margin-per-game"]
    game_stats = ["home-ap-rank-points", "away-ap-rank-points", 'home-pred-poll-rating', 'away-pred-poll-rating']
    for stat in stats_to_use:
        game_stats.append("home-" + stat + "-current")
        game_stats.append("away-" + stat + "-current")
    for game in gamedata:
        game_input = []
        for stat in game_stats:
            game_input.append(game.inputs[stat])
        all_inputs.append(game_input)
    all_inputs = [[float(x) for x in l] for l in all_inputs]
    all_outputs = [float(x) for x in all_outputs]
    return zip(all_inputs, all_outputs)



def retreive_all_dates(games):
    dates_to_games= defaultdict(list)
    for week in games:
        for game in week:
            game_date_object = game['start_date']
            split_object = game_date_object.rpartition('T')
            date = split_object[0]
            #time = split_object[2].rpartition('.')[0]
            dates_to_games[date].append(game)
    return dates_to_games


def combine_game_data(dates_to_games, polls, stats):
    input_data = []
    for date, games in dates_to_games.items():
        for game_info in games:
            season = game_info['season']
            week = game_info['week']
            key = str(season) + "," + str(week)
            ap_poll = polls.get('ap').get(key)
            coaches_poll = polls.get('coaches').get(key)
            # No talent data before 2015 for now
            # talent_rankings = []
            # for years_back in range(5):
            #     talent_rankings.append(talent[season-years_back])
            single_game_data = Game(date, game_info, ap_poll, coaches_poll, polls.get('predictive'))
            if single_game_data.valid:
                input_data.append(single_game_data)
    return input_data


def normalize(gamedata):
    keys = gamedata[0].inputs.keys()
    for key in keys:
        stats = [game.inputs[key] for game in gamedata]
        stat_mean = np.mean(stats)
        stat_std = np.std(stats)
        # max_stat = max(stats)
        # min_stat = min(stats)
        for game in gamedata:
            game.inputs[key] = (game.inputs[key] - stat_mean) / stat_std
    for game in gamedata:
        # decided to cut the week data
        game.inputs.pop("week")
    return gamedata


def save(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    frozen_data = []
    for game in data:
        frozen = jsonpickle.encode(game, max_depth=2)
        frozen_data.append(frozen)
    with open(path, 'w') as f:
        out = json.dumps(frozen_data)
        f.write(out)


def load(path):
    with open(path, 'r') as file:
        frozen = json.load(file)
        game_data = []
        for item in frozen:
            game_data.append(jsonpickle.decode(item))
    return game_data


def process_game_data(dates_to_games, polls, stats):
    print("Combining and normalizing game data...")
    game_data = combine_game_data(dates_to_games, polls, stats)
    return normalize(game_data)


def prepare_data():
    if file_access(GAME_DATA_PATH) and file_access(TEST_GAME_DATA_PATH):
        print("Loading existing game data")
        game_data = load(GAME_DATA_PATH)
    else:

        print("Running queries to download game data...")
        os.makedirs("training/data", exist_ok=True)
        print("Loading all games in the specified range...")
        games, test_games = games_query.query()

        dates_to_games, polls, stats = data_collector.collect_data(games)
        game_data = process_game_data(dates_to_games, polls, stats)
        print("Saving game data to", GAME_DATA_PATH)
        save(game_data, GAME_DATA_PATH)
        #
        # dates_to_games, polls, stats = data_collector.collect_data(test_games)
        # test_game_data = process_game_data(dates_to_games, polls, stats)
        # print("Saving test game data to", TEST_GAME_DATA_PATH)
        # save(test_game_data, TEST_GAME_DATA_PATH)

    all_data = list(create_netdata_from_gamedata(game_data))
    return split_datasets(all_data, pct_val=.2, pct_test=.1)

