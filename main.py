from queries import games_query, polls_query, stats_query
import jsonpickle
import os
import json
from collections import defaultdict
from game_data import Game
from global_config import file_access
from global_config import KERAS_MODEL_PATH
from models.conventionalNN import train_conventional
from models.tflow import train_net
import models.tflow as tflow
import numpy as np

GAME_DATA_PATH = "data/game_data.json"
TEST_GAME_DATA_PATH = "data/test_game_data.json"


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


def combine_game_data(dates_to_games, ap_polls, coaches_polls, pred_polls):
    input_data = []
    for date, games in dates_to_games.items():
        for game_info in games:
            season = game_info['season']
            week = game_info['week']
            key = str(season) + "," + str(week)
            ap_poll = ap_polls[key]
            coaches_poll = coaches_polls[key]
            # No talent data before 2015 for now
            # talent_rankings = []
            # for years_back in range(5):
            #     talent_rankings.append(talent[season-years_back])
            single_game_data = Game(date, game_info, ap_poll, coaches_poll, pred_polls)
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


def scikit_net(inputs, outputs, test_inputs, test_outputs):
    results = defaultdict(list)
    for test in range(10):
        results = train_conventional(inputs, outputs, test_inputs, test_outputs)
    for net_name, net_results in results.items():
        print(net_name)
        for i in range(len(net_results[0])):
            avg_val = np.mean([entry[i] for entry in net_results])
            print(avg_val)
        print("\n")


def tf_net(inputs, outputs, test_inputs, test_outputs):
    model, results = train_net(inputs, outputs, test_inputs, test_outputs, load=True)
    avg_val = np.mean(results)
    tflow.eval_net(model, test_inputs, test_outputs)
    print("Saving model to", KERAS_MODEL_PATH)
    model.save(KERAS_MODEL_PATH)
    print("Average off by", avg_val)


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
    return all_inputs, all_outputs


def main():
    if file_access(GAME_DATA_PATH) and file_access(TEST_GAME_DATA_PATH):
        print("Loading existing game data")
        game_data = load(GAME_DATA_PATH)
        test_game_data = load(TEST_GAME_DATA_PATH)
    else:
        print("Running queries to download game data...")
        os.makedirs("data", exist_ok=True)
        print("Loading all games in the specified range...")
        games, test_games = games_query.query()
        # talent = talent_query.query()
        print("Finding dates of games...")
        dates_to_games = retreive_all_dates(games)
        print("Loading historical polls...")
        ap_polls, coaches_polls, pred_polls = polls_query.query(dates_to_games)
        print("Loading historical statistics...")
        stats_query.query(dates_to_games)
        print("Combining and normalizing game data...")
        game_data = combine_game_data(dates_to_games, ap_polls, coaches_polls, pred_polls)
        game_data = normalize(game_data)
        print("Saving data to", GAME_DATA_PATH)
        save(game_data, GAME_DATA_PATH)

        # Repeat all that for test seasons
        print("Doing that all again for test seasons...")
        dates_to_games = retreive_all_dates(test_games)
        ap_polls, coaches_polls, pred_polls = polls_query.query(dates_to_games, append=True)
        stats_query.query(dates_to_games, append=True)
        test_game_data = combine_game_data(dates_to_games, ap_polls, coaches_polls, pred_polls)
        test_game_data = normalize(test_game_data)
        save(test_game_data, TEST_GAME_DATA_PATH)

    # game_data = game_data[:1000]
    all_inputs, all_outputs = create_netdata_from_gamedata(game_data)
    test_inputs, test_outputs = create_netdata_from_gamedata(test_game_data)
    # train_neat(all_inputs, all_outputs)
    print("Doing NN stuff...")

#   scikit_net(all_inputs, all_outputs, test_inputs, test_outputs)

    tf_net(all_inputs, all_outputs, test_inputs, test_outputs)




if __name__ == '__main__':
    main()
