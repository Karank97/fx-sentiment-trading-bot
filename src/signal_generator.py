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

def generate_signals():
    df = pd.read_csv(INPUT_FILE)
    df["text"] = df["title"].fillna("") + " " + df["description"].fillna("")
    df["text"] = df["text"].str.lower()

    currency_sentiment = defaultdict(list)

    for _, row in df.iterrows():
        for label_currency in set([cur for pair in CURRENCY_PAIRS.values() for cur in pair]):
            if label_currency in row["text"]:
                currency_sentiment[label_currency].append(row["compound"])

    results = []
    for pair, (base, quote) in CURRENCY_PAIRS.items():
        base_sentiment = sum(currency_sentiment[base]) / len(currency_sentiment[base]) if currency_sentiment[base] else 0
        quote_sentiment = sum(currency_sentiment[quote]) / len(currency_sentiment[quote]) if currency_sentiment[quote] else 0
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
