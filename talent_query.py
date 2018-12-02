import requests
import json
from global_config import years
from global_config import weeks
import os

PATH_JSON = 'data/talent.json'

def query():
    if os.path.isfile(PATH_JSON) and os.access(PATH_JSON, os.R_OK):
        with open(PATH_JSON) as file:
            talent = json.load(file)
            return talent
    first_year = min(years)
    last_year = max(years)
    talent_years = [year for year in range(first_year-4, last_year+1)]
    talent_by_year = {}
    for year in talent_years:

      #  url = "https://api.collegefootballdata.com/talent?year=" + str(year)
        url = "https://api.collegefootballdata.com/talent?year=2003"
        response = requests.get(url)
        talent = response.json()
        talent_by_year[year] = talent

    with open(PATH_JSON, 'w') as f:
        json.dump(talent_by_year, f)

    return talent_by_year
