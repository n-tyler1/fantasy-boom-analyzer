import pandas as pd
import time
from nba_api.stats.endpoints import playergamelog
from src.player_stats import get_top_players_by_fppg
from src.fantasy_points import compute_fantasy_points

SEASON = '2025-26'
BOOM_THRESHOLDS = [50, 60, 70, 80]

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

        # Exclusive bucket counts
        count_50_59 = ((logs['FANTASY_PTS'] >= 50) & (logs['FANTASY_PTS'] < 60)).sum()
        count_60_69 = ((logs['FANTASY_PTS'] >= 60) & (logs['FANTASY_PTS'] < 70)).sum()
        count_70_79 = ((logs['FANTASY_PTS'] >= 70) & (logs['FANTASY_PTS'] < 80)).sum()
        count_80_plus = (logs['FANTASY_PTS'] >= 80).sum()

        # Weighted score
        weighted_boom_score = (
            count_50_59 * 1 +
            count_60_69 * 2 +
            count_70_79 * 3 +
            count_80_plus * 4
        )

        boom_summary.append({
            'PLAYER_NAME': player['PLAYER_NAME'],
            'TEAM': player['TEAM_ABBREVIATION'],
            'GAMES': total_games,
            'MAX_SCORE': max_score,
            '50-59': count_50_59,
            '60-69': count_60_69,
            '70-79': count_70_79,
            '80+': count_80_plus,
            'WEIGHTED_BOOM': weighted_boom_score
        })

    df_summary = pd.DataFrame(boom_summary)
    df_summary = df_summary.sort_values('WEIGHTED_BOOM', ascending=False).reset_index(drop=True)
    return df_summary