import pandas as pd

FANTASY_SCORING = {
    'PTS': 1,
    'REB': 1,
    'AST': 2,
    'STL': 3,
    'BLK': 3
}

def compute_fantasy_points(df, scoring=FANTASY_SCORING):
    df = df.copy()
    df['FANTASY_PTS'] = (
        df['PTS'] * scoring['PTS'] +
        df['REB'] * scoring['REB'] +
        df['AST'] * scoring['AST'] +
        df['STL'] * scoring['STL'] +
        df['BLK'] * scoring['BLK']
    )
    return df