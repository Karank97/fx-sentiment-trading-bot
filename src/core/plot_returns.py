import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os
from pandas.tseries.offsets import BDay

CACHE_FILE = "data/price_cache.csv"

FX_TICKER_MAP = {
    "EUR/USD": "EURUSD=X",
    "USD/JPY": "JPY=X",
    "GBP/USD": "GBPUSD=X",
    "USD/CHF": "CHF=X",
    "AUD/USD": "AUDUSD=X",
    "USD/CAD": "CAD=X",
    "NZD/USD": "NZDUSD=X"
}

def fx_pair_to_yf(pair: str) -> str:
    return FX_TICKER_MAP.get(pair.strip().upper(), "")

def fetch_price_from_yahoo(ticker: str, timestamp: str) -> float:
    try:
        dt = pd.to_datetime(timestamp)

        if dt.weekday() >= 5:
            dt -= BDay(1)  # move to previous business day

        start = dt.strftime("%Y-%m-%d")
        end = (dt + timedelta(days=1)).strftime("%Y-%m-%d")
        df = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=False)

        if df.empty or 'Close' not in df:
            raise ValueError(f"No price data for {ticker} on {timestamp}")
        return float(df['Close'].iloc[0])  # fixed deprecated Series warning
    except Exception as e:
        print(f"❌ Error fetching {ticker} @ {timestamp}: {e}")
        return None

def calculate_returns(file_path):
    df = pd.read_csv(file_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    prices = []
    returns = []
    for _, row in df.iterrows():
        ticker = fx_pair_to_yf(row["pair"])
        price = fetch_price_from_yahoo(ticker, row["timestamp"])
        prices.append(price)

    df["entry_price"] = prices
    df["exit_price"] = df["entry_price"].shift(-1)  # assume next signal is exit
    df["return_pct"] = (df["exit_price"] - df["entry_price"]) / df["entry_price"] * 100
    df["cumulative_return"] = df["return_pct"].cumsum()

    return df, df["return_pct"], df["cumulative_return"]

def summarize_returns(returns):
    returns = returns.dropna()
    if returns.empty:
        return {
            "Total Return": 0,
            "Sharpe Ratio": 0,
            "Max Drawdown": 0,
            "Win Rate": 0
        }

    total_return = returns.sum()
    sharpe = returns.mean() / returns.std() * (252 ** 0.5) if returns.std() != 0 else 0
    max_drawdown = (returns.cumsum().cummax() - returns.cumsum()).max()
    win_rate = (returns > 0).sum() / len(returns)

    return {
        "Total Return": total_return,
        "Sharpe Ratio": sharpe,
        "Max Drawdown": max_drawdown,
        "Win Rate": win_rate
    }

def plot_cumulative_returns(cumulative_returns):
    fig, ax = plt.subplots(figsize=(10, 4))
    cumulative_returns.plot(ax=ax, title="Cumulative Return (%)")
    ax.set_ylabel("Return %")
    ax.grid(True)
    return fig
