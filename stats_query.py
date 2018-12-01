import requests
from global_config import statistics
import os
import _pickle as pickle
from collections import defaultdict
from bs4 import BeautifulSoup, NavigableString

PATH = 'data/stats.pkl'
def teams_in_games(games):
    teams = set()
    for game in games:
        home_team = game['home_team']
        away_team = game['away_team']
        teams.add(home_team)
        teams.add(away_team)
    return teams

def update_stats(stats, date, teams):
    for statistic in statistics:
        url = "https://www.teamrankings.com/college-football/stat/" + statistic + "?date="+ date
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        table_rows = soup.findAll('table')[0].findAll('tr')[1:]
        for row in table_rows:
            entries = row.contents
            if len(entries) is 16:
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
                    stats[(team, date)][statistic] = (team, rank, value, last_1, last_3, home, away, last_year)
    return stats

def query(dates_to_games):
    if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
        stats_in = open(PATH, 'rb')
        stats = pickle.load(stats_in)
        stats_in.close()
        return stats

    stats = defaultdict(dict)
    for date, games in dates_to_games.items():
        teams = teams_in_games(games)
        stats = update_stats(stats, date, teams)

    stats_out = open(PATH, 'wb')
    pickle.dump(stats, stats_out, -1)
    stats_out.close()

    return stats
