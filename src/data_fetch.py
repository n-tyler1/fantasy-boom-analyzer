from nba_api.stats.endpoints import leaguedashplayerstats
from src.fantasy_utils import compute_fantasy_points

SEASON = '2025-26'

def get_top_players_by_fppg(season=SEASON, top_n=50):
    df = leaguedashplayerstats.LeagueDashPlayerStats(
        season=season,
        season_type_all_star='Regular Season',
        per_mode_detailed='PerGame'
    ).get_data_frames()[0]

    df = compute_fantasy_points(df)
    df = df.sort_values('FANTASY_PTS', ascending=False).head(top_n)

    df = df[[
        'PLAYER_ID', 'PLAYER_NAME', 'TEAM_ABBREVIATION',
        'GP', 'MIN', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'FANTASY_PTS'
    ]]
    
    return df
