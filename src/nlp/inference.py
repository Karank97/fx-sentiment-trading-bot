import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os

INPUT_FILE = "data/raw_news.csv"
OUTPUT_FILE = "data/labeled_fx_news.csv"

def classify_sentiment(score, threshold=0.05):
    if score >= threshold:
        return "bullish"
    elif score <= -threshold:
        return "bearish"
    else:
        return "neutral"

def run_sentiment_analysis():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Input file not found: {INPUT_FILE}")
        return

    df = pd.read_csv(INPUT_FILE)

    required_cols = {"title", "description", "timestamp"}
    if not required_cols.issubset(df.columns):
        print(f"❌ Input file must contain {required_cols}")
        return

    analyzer = SentimentIntensityAnalyzer()

    results = []
    for _, row in df.iterrows():
        text = (str(row["title"]) + " " + str(row["description"])).strip()
        score = analyzer.polarity_scores(text)["compound"]
        label = classify_sentiment(score)

        results.append({
            "timestamp": row["timestamp"],
            "title": row["title"],
            "description": row["description"],
            "compound": score,
            "label": label
        })

    output_df = pd.DataFrame(results)
    output_df.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Labeled FX news saved to {OUTPUT_FILE}")
    print(output_df.head())

if __name__ == "__main__":
    run_sentiment_analysis()
