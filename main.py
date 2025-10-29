import sys
import os
from src.game_logs import analyze_boom_games

def main():
    print("Starting NBA Fantasy High Score Analysis...\n")

    # Step 1 → Analyze boom games for top 50 players
    df_boom = analyze_boom_games()

    # Step 2 → Save summary
    output_path = "data/player_boom_summary.csv"
    df_boom.to_csv(output_path, index=False)
    print(f"\nAnalysis complete! Saved to {output_path}\n")


    print("Top 10 Players by Max Fantasy Score:\n")
    print(df_boom.head(10))


if __name__ == "__main__":
    main()