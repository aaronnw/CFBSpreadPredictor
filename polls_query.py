import requests
import json
from global_config import year_from_date
from global_config import weeks
from global_config import resolve_team_name
from global_config import file_access
from stats_query import teams_in_games
from bs4 import BeautifulSoup, NavigableString
import os

PATH_AP_JSON = 'data/ap_poll.json'
PATH_COACHES_JSON = 'data/coaches_poll.json'
PATH_ALL_JSON = 'data/predictive_poll.json'

def update_pred_polls(pred_polls, date, teams):
    url = "https://www.teamrankings.com/college-football/ranking/predictive-by-other?date=" + date
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table_rows = soup.findAll('table')[0].findAll('tr')[1:]
    for row in table_rows:
        entries = row.contents
        if len(entries) == 19:
            rank = entries[1].contents[0]
            team = entries[3].contents[0]
            if type(team) is not NavigableString:
                team = team.contents[0]
            value = entries[5].contents[0]
            team = resolve_team_name(team)
            if team in teams:
                pred_polls[team + "," + date] = [rank, value]
    return pred_polls

def query(dates_to_games, append=False):
    if append == False and file_access(PATH_AP_JSON) and file_access(PATH_COACHES_JSON) and file_access(PATH_ALL_JSON):
        with open(PATH_AP_JSON) as file:
            ap_polls = json.load(file)
        with open(PATH_COACHES_JSON) as file:
            coaches_polls = json.load(file)
        with open(PATH_ALL_JSON) as file:
            pred_polls = json.load(file)
        return ap_polls, coaches_polls, pred_polls

    ap_polls = {}
    coaches_polls = {}
    pred_polls = {}
    game_years = set([year_from_date(date) for date in dates_to_games.keys()])
    for year in game_years:
        for week in weeks:
            headers = {
                'accept': 'application/json',
            }

            params = (
                ('seasons', str(year)),
                ('weeks', str(week))
            )

            response = requests.get('http://site.api.espn.com/apis/site/v2/sports/football/college-football/rankings', headers=headers, params=params)
            ap_poll_query = response.json()['rankings'][0]['ranks']
            coaches_poll_query = response.json()['rankings'][1]['ranks']
            ap_poll = {}
            coaches_poll = {}

            for pos in ap_poll_query:
                team_name = pos['team']['nickname']
                rank = pos['current']
                ap_poll[team_name] = rank

            for pos in coaches_poll_query:
                team_name = pos['team']['nickname']
                rank = pos['current']
                coaches_poll[team_name] = rank

            ap_polls[str(year) + "," + str(week)] = ap_poll
            coaches_polls[str(year) + "," + str(week)] = coaches_poll

    for date, games in dates_to_games.items():
        teams = teams_in_games(games)
        pred_polls = update_pred_polls(pred_polls, date, teams)

    if append:
        write = "w+"
    else:
        write = "w"

    with open(PATH_AP_JSON, write) as f:
        json.dump(ap_polls, f)

    with open(PATH_COACHES_JSON, write) as f:
        json.dump(coaches_polls, f)

    with open(PATH_ALL_JSON, write) as f:
        json.dump(pred_polls, f)

    return ap_polls, coaches_polls, pred_polls