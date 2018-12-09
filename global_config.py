year_range = (2007, 2007)
#Teams usually play 12 regular season games + one bye week + one week for rescheduled regular season games
#week_num = 14
week_num = 5
years = [year for year in range(year_range[0], year_range[1]+1)]
weeks = [week for week in range(1, week_num+1)]
statistics = ['average-scoring-margin', 'red-zone-scoring-pct', 'yards-per-play', 'third-down-conversion-pct',
              'average-team-passer-rating', 'yards-per-rush-attempt', 'opponent-red-zone-scoring-pct',
              'opponent-yards-per-play', 'opponent-third-down-conversion-pct', 'opponent-average-team-passer-rating',
              'opponent-yards-per-rush-attempt', 'turnover-margin-per-game', 'penalties-per-game']
STAT_PATH = "data/stats/"

# Convert the name used on teamrankings.com to match our other data
def resolve_team_name(team):
    if team == "LA Monroe":
        new_name = "Louisiana Monroe"
    elif team == "Miss State":
        new_name = "Mississippi State"
    elif team == "N Mex State":
        new_name = "New Mexico State"
    elif team == "Oregon St":
        new_name = "Oregon State"
    elif team == "Colorado St":
        new_name = "Colorado State"
    elif team == "Michigan St":
        new_name = "Michigan State"
    elif team == "Miami (FL)":
        new_name = "Miami"
    elif team == "VA Tech":
        new_name = "Virginia Tech"
    elif team == "GA Tech":
        new_name = "Georgia Tech"
    elif team == "GA Tech":
        new_name = "Georgia Tech"
    elif team == "Florida Intl":
        new_name = "Florida International"
    elif team == "App State":
        new_name = "Appalachian State"
    elif team == "W Kentucky":
        new_name = "Western Kentucky"
    elif team == "W Kentucky":
        new_name = "Western Kentucky"
    elif team == "Mississippi":
        new_name = "Ole Miss"
    elif team == "Boston Col":
        new_name = "Boston College"
    elif team == "Wash State":
        new_name = "Washington State"
    elif team == "Fla Atlantic":
        new_name = "Florida Atlantic"
    elif team == "Middle Tenn":
        new_name = "Middle Tennessee"
    elif team == "Central FL":
        new_name = "UCF"
    elif team == "TX Christian":
        new_name = "TCU"
    elif team == "E Michigan":
        new_name = "Eastern Michigan"
    elif team == "W Michigan":
        new_name = "Western Michigan"
    elif team == "N Carolina":
        new_name = "North Carolina"
    elif team == "Oklahoma St":
        new_name = "Oklahoma State"
    elif team == "S Mississippi":
        new_name = "Southern Mississippi"
    elif team == "Arkansas St":
        new_name = "Arkansas State"
    elif team == "Central Mich":
        new_name = "Central Michigan"
    elif team == "LA Tech":
        new_name = "Louisiana Tech"
    elif team == "S Carolina":
        new_name = "South Carolina"
    elif team == "LA Lafayette":
        new_name = "Louisiana"
    elif team == "S Florida":
        new_name = "South Florida"
    elif team == "Kansas St":
        new_name = "Kansas State"
    elif team == "Florida St":
        new_name = "Florida State"
    elif team == "N Illinois":
        new_name = "Northern Illinois"
    elif team == "W Virginia":
        new_name = "West Virginia"
    elif team == "Hawaii":
        new_name = "Hawai'i"
    elif team == "Arizona St":
        new_name = "Arizona State"
    elif team == "Fresno St":
        new_name = "Fresno State"
    elif team == "S Methodist":
        new_name = "SMU"
    elif team == "San Jose St":
        new_name = "San José State"
    elif team == "TX El Paso":
        new_name = "UTEP"
    elif team == "San Diego St":
        new_name = "San Diego State"
    elif team == "U Mass":
        new_name = "UMass"
    elif team == "Bowling Grn":
        new_name = "Bowling Green"
    else:
        return team
    return new_name