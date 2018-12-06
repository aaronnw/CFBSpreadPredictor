import games_query
import polls_query
import stats_query
import talent_query
import os
from collections import defaultdict
from game_data import Game
import _pickle as pickle
import neat

config_file = "neat.ini"
GAME_DATA_PATH = "data/game_data.pkl"
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

def combine_game_data(dates_to_games, ap_polls, coaches_polls):
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
            single_game_data = Game(date, game_info, ap_poll, coaches_poll)
            if single_game_data.valid:
                input_data.append(single_game_data)
    return input_data

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = 0


def train_net(game_data):
    all_inputs = [tuple(game.inputs.values()) for game in game_data]
    all_outputs = [game.output for game in game_data]
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    print(game_data)
    return True

def main():
    if os.path.isfile(GAME_DATA_PATH) and os.access(GAME_DATA_PATH, os.R_OK):
        with open(GAME_DATA_PATH, 'rb') as file:
            game_data = pickle.load(file)
    else:
        games = games_query.query()
        # talent = talent_query.query()
        ap_polls, coaches_polls = polls_query.query()
        dates_to_games = retreive_all_dates(games)
        stats_query.query(dates_to_games)
        game_data = combine_game_data(dates_to_games, ap_polls, coaches_polls)

        os.makedirs(os.path.dirname(GAME_DATA_PATH), exist_ok=True)
        with open(GAME_DATA_PATH, 'wb') as f:
            pickle.dump(game_data, f)
    net = train_net(game_data)

if __name__ == '__main__':
    main()