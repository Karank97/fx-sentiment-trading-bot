import pandas as pd
from collections import defaultdict

INPUT_FILE = "data/labeled_fx_news.csv"
OUTPUT_FILE = "data/fx_sentiment_signals.csv"

# Currency keywords to monitor
CURRENCY_PAIRS = {
    "EUR/USD": ("eur", "usd"),
    "USD/JPY": ("usd", "jpy"),
    "GBP/USD": ("gbp", "usd"),
    "USD/CHF": ("usd", "chf"),
    "AUD/USD": ("aud", "usd"),
    "USD/CAD": ("usd", "cad"),
    "NZD/USD": ("nzd", "usd")
}

# Define sentiment scores
SENTIMENT_SCORE = {
    "bullish": 1,
    "bearish": -1,
    "neutral": 0
}

def generate_signals():
    df = pd.read_csv(INPUT_FILE)
    
    if not {"title", "description", "label"}.issubset(df.columns):
        print("❌ Input file must contain 'title', 'description', and 'label' columns.")
        return

    df["text"] = df["title"].fillna("") + " " + df["description"].fillna("")
    df["text"] = df["text"].str.lower()

    currency_sentiment = defaultdict(list)

    for _, row in df.iterrows():
        sentiment_score = SENTIMENT_SCORE.get(row["label"], 0)
        for label_currency in set([cur for pair in CURRENCY_PAIRS.values() for cur in pair]):
            if label_currency in row["text"]:
                currency_sentiment[label_currency].append(sentiment_score)

    results = []
    for pair, (base, quote) in CURRENCY_PAIRS.items():
        base_scores = currency_sentiment[base]
        quote_scores = currency_sentiment[quote]
        
        base_sentiment = sum(base_scores) / len(base_scores) if base_scores else 0
        quote_sentiment = sum(quote_scores) / len(quote_scores) if quote_scores else 0
        net_sentiment = base_sentiment - quote_sentiment

        if net_sentiment > 0.1:
            signal = "LONG"
        elif net_sentiment < -0.1:
            signal = "SHORT"
        else:
            signal = "NEUTRAL"

        results.append({
            "pair": pair,
            "base_sentiment": round(base_sentiment, 4),
            "quote_sentiment": round(quote_sentiment, 4),
            "net_sentiment": round(net_sentiment, 4),
            "signal": signal
        })

    signals_df = pd.DataFrame(results)
    signals_df.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ FX Sentiment Signals saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_signals()
