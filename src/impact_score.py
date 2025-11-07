import pandas as pd

IMPACT_SCORING = {
    'PTS': 1,
    'REB': 1,
    'AST': 2,
    'STL': 3,
    'BLK': 3
}

def compute_impact_score(df, scoring=IMPACT_SCORING):
    df = df.copy()
    df['IMPACT_SCORE'] = (
        df['PTS'] * scoring['PTS'] +
        df['REB'] * scoring['REB'] +
        df['AST'] * scoring['AST'] +
        df['STL'] * scoring['STL'] +
        df['BLK'] * scoring['BLK']
    )
    return df