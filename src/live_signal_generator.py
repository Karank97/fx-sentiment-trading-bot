import re
import pandas as pd
from datetime import datetime
from inference import predict_sentiment
import os

LOG_FILE = "data/live_signals_log.csv"

CURRENCY_PAIRS = {
    "EUR/USD": ("eur", "usd"),
    "USD/JPY": ("usd", "jpy"),
    "GBP/USD": ("gbp", "usd"),
    "USD/CHF": ("usd", "chf"),
    "AUD/USD": ("aud", "usd"),
    "USD/CAD": ("usd", "cad"),
    "NZD/USD": ("nzd", "usd")
}

def identify_currency_pair(text):
    text = text.lower()
    found = []
    for pair, (base, quote) in CURRENCY_PAIRS.items():
        if base in text or quote in text:
            found.append((pair, base, quote))
    return found

def generate_trade_signal(title, description):
    result = predict_sentiment(title, description)
    text = f"{title} {description}".lower()
    predictions = []

    for pair, base, quote in identify_currency_pair(text):
        label = result["label"]
        if label == "positive":
            signal = f"LONG {pair}" if base in text else f"SHORT {pair}"
        elif label == "negative":
            signal = f"SHORT {pair}" if base in text else f"LONG {pair}"
        else:
            signal = f"NEUTRAL on {pair}"

        predictions.append({
            "timestamp": datetime.utcnow().isoformat(),
            "pair": pair,
            "title": title,
            "description": description,
            "label": label,
            "confidence": result["confidence"],
            "signal": signal
        })

    return predictions

def log_signals(predictions):
    df = pd.DataFrame(predictions)
    if not os.path.exists(LOG_FILE):
        df.to_csv(LOG_FILE, index=False)
    else:
        df.to_csv(LOG_FILE, mode="a", header=False, index=False)
    print(f"📝 Logged {len(df)} signal(s) to {LOG_FILE}")

if __name__ == "__main__":
    # Example headline
    title = "Yen weakens as BoJ holds rates steady"
    description = "JPY slides after Bank of Japan signals continued stimulus."

    predictions = generate_trade_signal(title, description)

    for s in predictions:
        print(f"📈 Signal: {s['signal']} | Sentiment: {s['label']} | Confidence: {s['confidence']}")
    log_signals(predictions)
