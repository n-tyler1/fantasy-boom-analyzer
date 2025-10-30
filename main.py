import sys
import os
from datetime import datetime
from src.game_logs import analyze_boom_games

def main():
    print("Starting NBA Fantasy Boom Score Analysis...\n")

    # Step 1: Analyze boom games for top 50 players by FPPG
    df_boom = analyze_boom_games()

    # Step 2: Save summary with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"data/player_boom_summary_{timestamp}.csv"
    df_boom.to_csv(output_path, index=False)
    print(f"\nAnalysis complete. Saved to {output_path}\n")


    print("Top 20 Players by Max Fantasy Score (with Boom Analysis):\n")
    print(df_boom.head(20))


if __name__ == "__main__":
    main()