import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

INPUT_FILE = "data/cleaned_fx_news.csv"
OUTPUT_FILE = "data/labeled_fx_news.csv"

def get_sentiment_label(score):
    if score >= 0.05:
        return "positive"
    elif score <= -0.05:
        return "negative"
    else:
        return "neutral"

def label_sentiment():
    df = pd.read_csv(INPUT_FILE)
    analyzer = SentimentIntensityAnalyzer()
    sentiments = []

    for _, row in df.iterrows():
        combined_text = f"{row['title']} {row['description']}"
        vs = analyzer.polarity_scores(combined_text)
        sentiments.append({
            "title": row["title"],
            "description": row["description"],
            "source": row["source"],
            "publishedAt": row["publishedAt"],
            "compound": vs["compound"],
            "label": get_sentiment_label(vs["compound"])
        })

    labeled_df = pd.DataFrame(sentiments)
    labeled_df.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Saved labeled sentiment data to {OUTPUT_FILE} — {len(labeled_df)} entries")

if __name__ == "__main__":
    label_sentiment()
