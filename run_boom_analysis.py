import sys
import os
from datetime import datetime
from src.boom_analysis import analyze_boom_games

def main():
    print("=== NBA Fantasy Boom Score Analysis ===")

    # Step 1: Analyze boom games for top players by FPPG
    print("Analyzing boom games for top players...")
    df_boom = analyze_boom_games()

    # Step 2: Save summary with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_path = f"data/player_boom_summary_{timestamp}.csv"
    df_boom.to_csv(output_path, index=False)
    print(f"\nAnalysis complete, results saved to: {output_path}\n")

    # Step 3: Display top-performing players and their boom stats
    print("Top 20 Players by Max Fantasy Score (Boom Analysis):\n")
    print(df_boom.head(20))


if __name__ == "__main__":
    main()