import sys
import os
from datetime import datetime
from src.impact_analysis import analyze_impact_games
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    print("=== NBA Player Impact Analysis ===")

    # Step 1: Analyze impact games for top players by FPPG
    print("Analyzing high-impact performances for top players...")
    df_impact = analyze_impact_games()

    # Step 2: Save summary with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_path = f"data/player_impact_summary_{timestamp}.csv"
    df_impact.to_csv(output_path, index=False)
    print(f"\nAnalysis complete, results saved to: {output_path}\n")

    # Step 3: Display top-performing players and their impact stats
    print("Top 20 Players by Weighted Impact Score:\n")
    print(df_impact.head(20))

if __name__ == "__main__":
    main()