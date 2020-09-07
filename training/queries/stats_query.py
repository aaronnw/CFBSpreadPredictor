import requests
from global_config import statistics
from global_config import STAT_PATH
from global_config import resolve_team_name
from global_config import years
from utils import file_access, year_from_date
import os
import json
from bs4 import BeautifulSoup, NavigableString


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
            team = resolve_team_name(team)
            if team in teams:
                stats[team +","+ date] = [rank, value, last_1, last_3, home, away, last_year]
    return stats


def stat_files_exist():
    for statistic in statistics:
        for year in years:
            stat_file = STAT_PATH+ statistic + str(year) + ".json"
            if not file_access(stat_file):
                return False
    return True


def query(dates_to_games, append = False):
    for statistic in statistics:
        game_years = set([year_from_date(date) for date in dates_to_games.keys()])
        for year in game_years:
            stat_file = STAT_PATH + statistic + str(year) + ".json"
            if append == True or not file_access(stat_file):
                stats = {}
                games_in_year = [(date, dates_to_games[date]) for date in dates_to_games.keys() if year_from_date(date) == str(year)]
                for date, games in games_in_year:
                    teams = teams_in_games(games)
                    stats = update_stats(stats, statistic, date, teams)

                stat_file = STAT_PATH + statistic + str(year) +".json"
                os.makedirs(os.path.dirname(stat_file), exist_ok=True)
                with open(stat_file, 'w+') as f:
                    json.dump(stats, f)