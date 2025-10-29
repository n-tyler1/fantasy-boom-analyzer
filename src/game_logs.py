import pandas as pd
import time
from nba_api.stats.endpoints import playergamelog
from src.data_fetch import get_top_players_by_fppg
from src.fantasy_utils import compute_fantasy_points

SEASON = '2025-26'
BOOM_THRESHOLDS = [50, 60, 70, 80, 90]

def get_player_game_logs(player_id, season=SEASON):
    time.sleep(0.6)
    logs = playergamelog.PlayerGameLog(
        player_id=player_id,
        season=season,
        season_type_all_star='Regular Season'
    ).get_data_frames()[0]
    return logs

def analyze_boom_games(thresholds=BOOM_THRESHOLDS):
    top_players = get_top_players_by_fppg(season=SEASON, top_n=50)
    boom_summary = []

    for _, player in top_players.iterrows():
        logs = get_player_game_logs(player['PLAYER_ID'])
        logs = compute_fantasy_points(logs)

        total_games = len(logs)
        max_score = logs['FANTASY_PTS'].max()

        boom_counts = {}
        for t in thresholds:
            boom_counts[f'Over_{t}'] = (logs['FANTASY_PTS'] >= t).sum()

        boom_summary.append({
            'PLAYER_NAME': player['PLAYER_NAME'],
            'TEAM': player['TEAM_ABBREVIATION'],
            'GAMES': total_games,
            'MAX_SCORE': max_score,
            **boom_counts
        })

    df_summary = pd.DataFrame(boom_summary)
    df_summary = df_summary.sort_values('MAX_SCORE', ascending=False).reset_index(drop=True)
    return df_summary

if __name__ == "__main__":
    df_boom = analyze_boom_games()
    print(df_boom.head(20))