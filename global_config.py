year_range = (2015, 2019)

# Teams usually play 12 regular season games + one bye week + one week for rescheduled regular season games
# week_num = 14
week_num = 14
years = [year for year in range(year_range[0], year_range[1] + 1)]
weeks = [week for week in range(1, week_num+1)]
statistics = ['average-scoring-margin', 'red-zone-scoring-pct', 'yards-per-play', 'third-down-conversion-pct',
              'average-team-passer-rating', 'yards-per-rush-attempt', 'opponent-red-zone-scoring-pct',
              'opponent-yards-per-play', 'opponent-third-down-conversion-pct', 'opponent-average-team-passer-rating',
              'opponent-yards-per-rush-attempt', 'turnover-margin-per-game', 'penalties-per-game']


STAT_PATH = "data/stats/"
GAME_DATA_PATH = "data/game_data.json"
TEST_GAME_DATA_PATH = "data/test_game_data.json"
KERAS_MODEL_PATH = "models/keras_model.h5"


team_rankings_dict = {
    "LA Monroe": "Louisiana Monroe",
    "Miss State": "Mississippi State",
    "N Mex State": "New Mexico State",
    "Oregon St": "Oregon State",
    "Colorado St": "Colorado State",
    "Michigan St": "Michigan State",
    "Miami (FL)":" Miami",
    "VA Tech": "Virginia Tech",
    "GA Tech": "Georgia Tech",
    "Florida Intl": "Florida International",
    "App State": "Appalachian State",
    "W Kentucky": "Western Kentucky",
    "Mississippi": "Ole Miss",
    "Boston Col": "Boston College",
    "Wash State": "Washington State",
    "Fla Atlantic": "Florida Atlantic",
    "Middle Tenn": "Middle Tennessee",
    "Central FL": "UCF",
    "TX Christian": "TCU",
    "E Michigan": "Eastern Michigan",
    "W Michigan": "Western Michigan",
    "N Carolina": "North Carolina",
    "Oklahoma St": "Oklahoma State",
    "S Mississippi": "Southern Mississippi",
    "Arkansas St": "Arkansas State",
    "Central Mich": "Central Michigan",
    "LA Tech": "Louisiana Tech",
    "S Carolina": "South Carolina",
    "LA Lafayette": "Louisiana",
    "S Florida": "South Florida",
    "Kansas St": "Kansas State",
    "Florida St": "Florida State",
    "N Illinois": "Northern Illinois",
    "W Virginia": "West Virginia",
    "Hawaii": "Hawai'i",
    "Arizona St": "Arizona State",
    "Fresno St": "Fresno State",
    "S Methodist": "SMU",
    "San Jose St": "San José State",
    "TX El Paso": "UTEP",
    "San Diego St": "San Diego State",
    "U Mass": "UMass",
    "Bowling Grn": "Bowling Green",
    "TX-San Ant": "UT San Antonio",
    "GA Southern": "Georgia Southern",
    "S Alabama": "South Alabama",
    "E Carolina": "East Carolina"
}


# Convert the name used on teamrankings.com to match our other data
def resolve_team_name(team):
    return team_rankings_dict.get(team, team)
