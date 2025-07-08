#!/usr/bin/env python3
# scripts/populate_returns.py

import os
from datetime import timedelta
import pandas as pd
import yfinance as yf

LOG_FILE       = "data/live_signals_log.csv"
CONF_THRESHOLD = 0.75

PAIR_TO_YF = {
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "USD/JPY": "JPY=X",
    "USD/CHF": "CHF=X",
    "AUD/USD": "AUDUSD=X",
    "USD/CAD": "CAD=X",
    "NZD/USD": "NZDUSD=X"
}

def fx_pair_to_yf(pair):
    return PAIR_TO_YF.get(pair)

def main():
    # — load signals —
    df = pd.read_csv(LOG_FILE, parse_dates=["timestamp"])
    # reset return columns
    df["return_pct"]        = 0.0
    df["cumulative_return"] = 0.0

    # select only the signals we actually want to compute
    mask = (df["confidence"].fillna(0) >= CONF_THRESHOLD) & \
           (df["label"].str.lower() != "neutral")
    df_calc = df.loc[mask, ["timestamp","pair","label"]]

    # build a map: pair → set of dates (entry day and exit day)
    pair_dates = {}
    for ts, pair, label in df_calc.itertuples(index=False):
        d0 = ts.date()
        d1 = (ts + timedelta(days=1)).date()
        pair_dates.setdefault(pair, set()).update([d0, d1])

    # batch-download all required prices for each pair
    price_map = {}  # (pair, date) → price
    for pair, dates in pair_dates.items():
        ticker = fx_pair_to_yf(pair)
        if not ticker:
            print(f"⚠️  Unknown pair {pair}, skipping")
            continue

        dt0 = min(dates)
        dt1 = max(dates) + timedelta(days=1)
        print(f"📥 Downloading {pair} ({ticker}) from {dt0} to {dt1}")
        raw = yf.download(ticker,
                          start=dt0.strftime("%Y-%m-%d"),
                          end=(dt1 + timedelta(days=1)).strftime("%Y-%m-%d"),
                          progress=False)

        if raw.empty or "Close" not in raw:
            print(f"⚠️  No data for {pair} in that range, skipping")
            continue

        # index → pandas.Timestamp; convert to date
        closes = raw["Close"]
        for dt in dates:
            # find the first row whose date matches dt
            matches = closes.loc[closes.index.date == dt]
            if not matches.empty:
                price_map[(pair, dt)] = float(matches.iloc[0])

    # now compute returns row by row
    cum = 0.0
    for i, row in df.iterrows():
        label = str(row.get("label","")).lower()
        conf  = float(row.get("confidence", 0))
        pair  = row["pair"]
        ts    = row["timestamp"]
        if conf < CONF_THRESHOLD or label == "neutral":
            df.at[i, "cumulative_return"] = cum
            continue

        d0 = ts.date()
        d1 = (ts + timedelta(days=1)).date()
        p0 = price_map.get((pair, d0), None)
        p1 = price_map.get((pair, d1), None)

        if p0 is None or p1 is None or p0 == 0:
            ret_pct = 0.0
        else:
            ret = (p1 - p0)/p0 if label=="positive" else (p0 - p1)/p0
            ret_pct = ret * 100

        cum += ret_pct
        df.at[i, "return_pct"]        = ret_pct
        df.at[i, "cumulative_return"] = cum

    # overwrite the CSV
    df.to_csv(LOG_FILE, index=False)
    print(f"✅ Filled return_pct & cumulative_return in {LOG_FILE}")

if __name__=="__main__":
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    main()
