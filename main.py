import games_query
import polls_query
import stats_query
from collections import defaultdict

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

def main():
    games = games_query.query()
    dates_to_games = retreive_all_dates(games)
    stats_query.query(dates_to_games)
    print(dates_to_games)
    # polls_query.query()
    # rankings_query.query()

if __name__ == '__main__':
    main()