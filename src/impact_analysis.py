import pandas as pd
import time
from nba_api.stats.endpoints import playergamelog
from src.player_stats import get_top_players_by_fppg
from src.impact_score import compute_impact_score

SEASON = '2025-26'
SCORE_THRESHOLDS = [50, 60, 70, 80, 90, 100]

def get_player_game_logs(player_id, season=SEASON):
    time.sleep(0.6)
    logs = playergamelog.PlayerGameLog(
        player_id=player_id,
        season=season,
        season_type_all_star='Regular Season'
    ).get_data_frames()[0]
    return logs

def analyze_impact_games(thresholds=SCORE_THRESHOLDS):
    top_players = get_top_players_by_fppg(season=SEASON, top_n=50)
    impact_summary = []

    for _, player in top_players.iterrows():
        logs = get_player_game_logs(player['PLAYER_ID'])
        logs = compute_impact_score(logs)

        total_games = len(logs)
        top_3_scores = logs['IMPACT_SCORE'].nlargest(3).tolist()

        # Exclusive bucket counts
        count_50_59 = ((logs['IMPACT_SCORE'] >= 50) & (logs['IMPACT_SCORE'] < 60)).sum()
        count_60_69 = ((logs['IMPACT_SCORE'] >= 60) & (logs['IMPACT_SCORE'] < 70)).sum()
        count_70_79 = ((logs['IMPACT_SCORE'] >= 70) & (logs['IMPACT_SCORE'] < 80)).sum()
        count_80_89 = ((logs['IMPACT_SCORE'] >= 80) & (logs['IMPACT_SCORE'] < 90)).sum()
        count_90_99 = ((logs['IMPACT_SCORE'] >= 90) & (logs['IMPACT_SCORE'] < 100)).sum()
        count_100_plus = (logs['IMPACT_SCORE'] >= 100).sum()

        # Weighted score
        weighted_impact_score = (
            count_50_59 * 1 +
            count_60_69 * 2 +
            count_70_79 * 3 +
            count_80_89 * 4 +
            count_90_99 * 5 +
            count_100_plus * 6
        )

        impact_summary.append({
            'PLAYER_NAME': player['PLAYER_NAME'],
            'TEAM': player['TEAM_ABBREVIATION'],
            'GAMES': total_games,
            'TOP_SCORES': top_3_scores,
            '50-59': count_50_59,
            '60-69': count_60_69,
            '70-79': count_70_79,
            '80-89': count_80_89,
            '90-99': count_90_99,
            '100+': count_100_plus,
            'WEIGHTED_IMPACT': weighted_impact_score
        })

    df_summary = pd.DataFrame(impact_summary)
    df_summary = df_summary.sort_values('WEIGHTED_IMPACT', ascending=False).reset_index(drop=True)
    return df_summary