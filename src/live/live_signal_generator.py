import csv
import os
from datetime import datetime, timedelta

from core.plot_returns import fx_pair_to_yf, fetch_price_from_yahoo, get_cached_price, cache_price

LOG_FILE = "data/live_signals_log.csv"
CONF_THRESH = 0.75

# Ensure data folder exists
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def initialize_log():
    """Create log with headers if it doesn't exist."""
    if not os.path.isfile(LOG_FILE):
        with open(LOG_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp", "pair", "title", "description",
                "label", "confidence", "signal",
                "entry_price", "exit_price",
                "return_pct", "cumulative_return"
            ])

def log_signals(signals):
    """
    signals: iterable of dicts with keys
    ['timestamp','pair','title','description','label','confidence','signal']
    """
    initialize_log()
    cumulative = 0.0

    try:
        with open(LOG_FILE, newline="") as f:
            reader = list(csv.DictReader(f))
            if reader:
                cumulative = float(reader[-1]["cumulative_return"])
    except Exception:
        pass

    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)

        for sig in signals:
            ts = sig["timestamp"]
            pair = sig["pair"]
            lbl = sig["label"].lower()
            conf = float(sig["confidence"])

            # 1) Quality filter
            if conf < CONF_THRESH or lbl == "neutral":
                continue

            ticker = fx_pair_to_yf(pair)
            if not ticker:
                continue

            # 2) Fetch entry price
            entry = get_cached_price(pair, ts)
            if entry is None:
                entry = fetch_price_from_yahoo(ticker, ts)
                if entry is not None:
                    cache_price(pair, ts, entry)

            # 3) Fetch exit price (1 day later)
            exit_ts = ts + timedelta(days=1)
            exit_p = get_cached_price(pair, exit_ts)
            if exit_p is None:
                exit_p = fetch_price_from_yahoo(ticker, exit_ts)
                if exit_p is not None:
                    cache_price(pair, exit_ts, exit_p)

            # 4) Compute return_pct
            if entry and exit_p and entry != 0:
                raw_ret = (exit_p - entry) / entry
                ret_pct = raw_ret * 100 if lbl == "positive" else -raw_ret * 100
            else:
                ret_pct = 0.0

            # 5) Update cumulative
            cumulative += ret_pct

            # 6) Write row
            writer.writerow([
                ts, pair, sig["title"], sig["description"],
                sig["label"], sig["confidence"], sig["signal"],
                f"{entry:.6f}" if entry else "",
                f"{exit_p:.6f}" if exit_p else "",
                f"{ret_pct:.4f}",
                f"{cumulative:.4f}",
            ])

# ---------------------- SIGNAL GENERATION ----------------------

CURRENCY_PAIRS = {
    "EUR/USD": ("eur", "usd"),
    "USD/JPY": ("usd", "jpy"),
    "GBP/USD": ("gbp", "usd"),
    "USD/CHF": ("usd", "chf"),
    "AUD/USD": ("aud", "usd"),
    "USD/CAD": ("usd", "cad"),
    "NZD/USD": ("nzd", "usd")
}

def generate_trade_signal(title, description):
    """
    Generate trade signal(s) from article text.
    Returns a list of signal dicts for each pair mentioned.
    """
    text = (str(title or "") + " " + str(description or "")).lower()
    signals = []

    for pair, (base, quote) in CURRENCY_PAIRS.items():
        if base in text or quote in text:
            label = "neutral"
            confidence = 0.0
            signal = "NEUTRAL"

            if any(word in text for word in ["rally", "bullish", "optimism", "gain", "surge", "strong", "hawkish"]):
                label = "positive"
                confidence = 0.85
                signal = "LONG"
            elif any(word in text for word in ["fall", "bearish", "drop", "decline", "recession", "weak", "dovish"]):
                label = "negative"
                confidence = 0.85
                signal = "SHORT"

            signals.append({
                "timestamp": datetime.utcnow(),
                "pair": pair,
                "title": title,
                "description": description,
                "label": label,
                "confidence": confidence,
                "signal": signal
            })

    return signals
