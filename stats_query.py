import requests
from global_config import statistics
from global_config import STAT_PATH
import os
import json
import _pickle as pickle
from collections import defaultdict
from bs4 import BeautifulSoup, NavigableString
import sys

def teams_in_games(games):
    teams = set()
    for game in games:
        home_team = game['home_team']
        away_team = game['away_team']
        teams.add(home_team)
        teams.add(away_team)
    return teams

def update_stats(stats, statistic, date, teams):
    url = "https://www.teamrankings.com/college-football/stat/" + statistic + "?date="+ date
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table_rows = soup.findAll('table')[0].findAll('tr')[1:]
    for row in table_rows:
        entries = row.contents
        if len(entries) == 17:
            rank = entries[1].contents[0]
            team = entries[3].contents[0]
            if type(team) is not NavigableString:
                team = team.contents[0]
            value = entries[5].contents[0]
            last_3 = entries[7].contents[0]
            last_1 = entries[9].contents[0]
            home = entries[11].contents[0]
            away = entries[13].contents[0]
            last_year = entries[15].contents[0]
            if team in teams:
                stats[team +","+ date] = [rank, value, last_1, last_3, home, away, last_year]
    return stats

def stat_files_exist():
    for statistic in statistics:
        stat_file = STAT_PATH+statistic+".json"
        if not (os.path.isfile(stat_file) and os.access(stat_file, os.R_OK)):
            return False
    return True

def query(dates_to_games):
    if stat_files_exist():
        return
    else:
        for statistic in statistics:
            stats = {}
            for date, games in dates_to_games.items():
                teams = teams_in_games(games)
                stats = update_stats(stats, statistic, date, teams)

            stat_file = STAT_PATH + statistic + ".json"
            os.makedirs(os.path.dirname(stat_file), exist_ok=True)
            with open(stat_file, 'w') as f:
                json.dump(stats, f)
