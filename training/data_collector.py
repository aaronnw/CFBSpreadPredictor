import os
from collections import defaultdict

from training.queries import games_query, polls_query, stats_query

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


def collect_data(games):
    # talent = talent_query.query()
    print("Finding dates of games...")
    dates_to_games = retreive_all_dates(games)
    print("Loading historical polls...")
    ap_polls, coaches_polls, pred_polls = polls_query.query(dates_to_games)
    polls = {"ap": ap_polls, "coaches": coaches_polls, "predictive": pred_polls}
    print("Loading historical statistics...")
    stats = stats_query.query(dates_to_games)
    return dates_to_games, polls, stats

