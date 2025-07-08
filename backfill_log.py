import pandas as pd
from datetime import timedelta
import yfinance as yf
import os

LOG_PATH = "data/live_signals_log.csv"

FX_YAHOO_TICKER_MAP = {
    "EUR/USD": "EURUSD=X",
    "USD/JPY": "JPY=X",
    "GBP/USD": "GBPUSD=X",
    "USD/CHF": "CHF=X",
    "AUD/USD": "AUDUSD=X",
    "USD/CAD": "CAD=X",
    "NZD/USD": "NZDUSD=X"
}

def fetch_price(ticker: str, timestamp: pd.Timestamp) -> float:
    """Fetch the close price of the FX ticker at the signal timestamp."""
    start = timestamp - timedelta(days=1)
    end = timestamp + timedelta(days=1)
    df = yf.download(ticker, start=start, end=end, progress=False)
    if df.empty:
        return None
    # Find the row closest to the timestamp
    df.index = pd.to_datetime(df.index)
    df['diff'] = abs(df.index - timestamp)
    closest = df.loc[df['diff'].idxmin()]
    return float(closest['Close'])

def backfill_log():
    if not os.path.exists(LOG_PATH):
        print(f"File not found: {LOG_PATH}")
        return

    df = pd.read_csv(LOG_PATH, parse_dates=["timestamp"])
    df.sort_values("timestamp", inplace=True)
    df.reset_index(drop=True, inplace=True)

    cumulative = 0.0

    for i, row in df.iterrows():
        updated = False
        if pd.isna(row.get("entry_price")):
            ticker = FX_YAHOO_TICKER_MAP.get(row["currency_pair"])
            if not ticker:
                continue
            price = fetch_price(ticker, row["timestamp"])
            if price is not None:
                df.at[i, "entry_price"] = price
                updated = True

        if updated or pd.isna(row.get("return_pct")):
            sentiment = row["sentiment"]
            if sentiment in ("bullish", "bearish") and pd.notna(df.at[i, "entry_price"]):
                direction = 1 if sentiment == "bullish" else -1
                target = fetch_price(FX_YAHOO_TICKER_MAP.get(row["currency_pair"]), row["timestamp"] + timedelta(days=1))
                if target:
                    entry = df.at[i, "entry_price"]
                    return_pct = (target - entry) / entry * direction * 100
                    df.at[i, "return_pct"] = return_pct
                    cumulative += return_pct
                    df.at[i, "cumulative_return"] = cumulative

    df.to_csv(LOG_PATH, index=False)
    print(f"✅ Backfill complete. Updated file saved to: {LOG_PATH}")

if __name__ == "__main__":
    backfill_log()
