from global_config import statistics
from global_config import STAT_PATH
import  os
import json


def get_poll_rank_points(poll, team):
    points = 0
    if team in poll.keys():
        points = 26 - poll[team]
    return points

def without_percent(s):
    if '%' not in s:
        return s
    else:
        return s.replace("%", "")

def parse_stat_line(stat_list):
    results = {}
    # Comes in the form: Current year | last 3 | last 1 | Home | Away | Last year

    #Remove the rank value for now
    stat_list = stat_list[1:]
    #First remove percentage values
    stat_list = [without_percent(s) for s in stat_list]

    #If no last year data, start with 0
    last_year = stat_list[len(stat_list) - 1]
    if last_year == '--':
        stat_list[len(stat_list)-1] = '0'

    #If no this year data, start with last years
    if stat_list[0] == '--':
        stat_list[0] = stat_list[len(stat_list)-1]

    for item_index in range(1, len(stat_list)-1):
        if stat_list[item_index] == '--':
            stat_list[item_index] = stat_list[0]

    #Shouldn't have any blanks yet, so convert to floats
    stat_list = [float(s) for s in stat_list]


    results["current"] = stat_list[1]
    results["last3"] = stat_list[2]
    results["last1"] = stat_list[3]
    results["home"] = stat_list[4]
    results["away"] = stat_list[5]
    return results

class Game:
    #If everything checks out, this stays true
    valid : bool
    #Inputs to net
    inputs : {}
    #Spread for home team
    output : int
    def __init__(self, date, game_info, ap_poll, coaches_poll):
        self.valid = True
        home_team = game_info['home_team']
        away_team = game_info['away_team']
        season = game_info['season']
        week = game_info['week']
        self.inputs = {}
        self.output = game_info['home_points'] - game_info['away_points']
        self.inputs['week'] = week
        self.inputs['home_ap_rank_points'] = get_poll_rank_points(ap_poll, home_team)
        self.inputs['away_ap_rank_points'] = get_poll_rank_points(ap_poll, away_team)
        self.inputs['home_coaches_rank_points'] = get_poll_rank_points(coaches_poll, home_team)
        self.inputs['away_coaches_rank_points'] = get_poll_rank_points(coaches_poll, away_team)
        for stat in statistics:
            #Load the statistic from a file
            stat_file = STAT_PATH + stat + ".json"
            if os.path.isfile(stat_file) and os.access(stat_file, os.R_OK):
                with open(stat_file) as file:
                    stats = json.load(file)

            if home_team+","+date in stats and away_team+","+date in stats:
                home_stats = parse_stat_line(stats[home_team+","+date])
                self.inputs["home-" + stat + "-current"] = home_stats["current"]
                self.inputs["home-" + stat + "-last3"] = home_stats["last3"]
                self.inputs["home-" + stat + "-home"] = home_stats["home"]
                self.inputs["home-" + stat + "-away"] = home_stats["away"]

                away_stats = parse_stat_line(stats[away_team + "," + date])
                self.inputs["away-" + stat + "-current"] = away_stats["current"]
                self.inputs["away-" + stat + "-last3"] = away_stats["last3"]
                self.inputs["away-" + stat + "-away"] = away_stats["away"]
                self.inputs["away-" + stat + "-away"] = away_stats["away"]
            else:
                self.valid = False



