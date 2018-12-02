year_range = (2007, 2017)
#Teams usually play 12 regular season games + one bye week + one week for rescheduled regular season games
week_num = 14
years = [year for year in range(year_range[0], year_range[1]+1)]
weeks = [week for week in range(1, week_num+1)]
statistics = ['average-scoring-margin', 'red-zone-scoring-pct', 'yards-per-play', 'third-down-conversion-pct',
              'average-team-passer-rating', 'yards-per-rush-attempt', 'opponent-red-zone-scoring-pct',
              'opponent-yards-per-play', 'opponent-third-down-conversion-pct', 'opponent-average-team-passer-rating',
              'opponent-yards-per-rush-attempt', 'turnover-margin-per-game', 'penalties-per-game']
STAT_PATH = "data/stats/"