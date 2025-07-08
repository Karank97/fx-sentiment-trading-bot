# scripts/check_signal_counts.py

import pandas as pd

def main():
    # load your live‐signals log
    df = pd.read_csv("data/live_signals_log.csv", parse_dates=["timestamp"])
    
    # make sure confidence column is numeric
    df["confidence"] = pd.to_numeric(df.get("confidence", 0), errors="coerce").fillna(0)
    
    # total
    total = len(df)
    # how many with confidence ≥0.75
    high_conf = (df["confidence"] >= 0.75).sum()
    # how many non‐neutral
    labels = df["label"].astype(str).str.lower()
    non_neutral = (labels != "neutral").sum()
    # how many survive both filters
    survivors = df[(df["confidence"] >= 0.75) & (labels != "neutral")]
    
    print(f"Total signals               : {total}")
    print(f"Signals ≥ 0.75 confidence   : {high_conf}")
    print(f"Signals non‐neutral label   : {non_neutral}")
    print(f"Passing both filters        : {len(survivors)}")
    print("\nUnique labels in your CSV:", df["label"].unique())
    print("\nExample survivors:\n", survivors.head())

if __name__ == "__main__":
    main()
