import games_query
import polls_query
import stats_query
import talent_query
import jsonpickle
import os
import json
from collections import defaultdict
from game_data import Game
from neat import train_neat
from conventionalNN import train_conventional
import random

GAME_DATA_PATH = "data/game_data.json"

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
        max_stat = max(stats)
        min_stat = min(stats)
        for game in gamedata:
            game.inputs[key] = (game.inputs[key] - min_stat) / (max_stat-min_stat)
    for game in gamedata:
        # decided to cut the week data
        game.inputs.pop("week")
    return gamedata

def save(game_data):
    os.makedirs(os.path.dirname(GAME_DATA_PATH), exist_ok=True)
    frozen_data = []
    for game in game_data:
        frozen = jsonpickle.encode(game, max_depth=2)
        frozen_data.append(frozen)
    with open(GAME_DATA_PATH, 'w') as f:
        out = json.dumps(frozen_data)
        f.write(out)


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
    return all_inputs, all_outputs

def main():
    if os.path.isfile(GAME_DATA_PATH) and os.access(GAME_DATA_PATH, os.R_OK):
        with open(GAME_DATA_PATH, 'r') as file:
            frozen = json.load(file)
            game_data = []
            for item in frozen:
                game_data.append(jsonpickle.decode(item))
    else:
        os.makedirs("data", exist_ok=True)
        games = games_query.query()
        # talent = talent_query.query()
        dates_to_games = retreive_all_dates(games)
        ap_polls, coaches_polls, pred_polls = polls_query.query(dates_to_games)
        stats_query.query(dates_to_games)
        game_data = combine_game_data(dates_to_games, ap_polls, coaches_polls, pred_polls)
        game_data = normalize(game_data)
        save(game_data)
    #game_data = game_data[:1000]
    #train_neat(all_inputs, all_outputs)
    for test in range(10):
        test_set = [random.choice(game_data) for x in range(1000)]
        all_inputs, all_outputs = create_netdata_from_gamedata(test_set)
        train_conventional(all_inputs, all_outputs)

if __name__ == '__main__':
    main()