from nba_api.stats.endpoints import leaguedashplayerstats
from src.impact_score import compute_impact_score

SEASON = '2025-26'

def get_top_players_by_fppg(season=SEASON, top_n=50):
    df = leaguedashplayerstats.LeagueDashPlayerStats(
        season=season,
        season_type_all_star='Regular Season',
        per_mode_detailed='PerGame'
    ).get_data_frames()[0]

    df = compute_impact_score(df)
    df = df.sort_values('IMPACT_SCORE', ascending=False).head(top_n)

    df = df[[
        'PLAYER_ID', 'PLAYER_NAME', 'TEAM_ABBREVIATION',
        'GP', 'MIN', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'IMPACT_SCORE'
    ]]
    
    return df