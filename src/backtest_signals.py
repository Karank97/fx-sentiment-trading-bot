import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import os

SIGNAL_FILE = "data/fx_sentiment_signals.csv"
PRICE_LOOKBACK_DAYS = 10
HOLD_PERIOD_DAYS = 3
INITIAL_CAPITAL = 100000

PAIR_TO_YF = {
    "EUR/USD": "EURUSD=X",
    "USD/JPY": "JPY=X",
    "GBP/USD": "GBPUSD=X",
    "USD/CHF": "CHF=X",
    "AUD/USD": "AUDUSD=X",
    "USD/CAD": "CAD=X",
    "NZD/USD": "NZDUSD=X"
}

def fetch_price_data(ticker, start_date, end_date):
    print(f"📈 Downloading {ticker} from {start_date} to {end_date}...")
    df = yf.download(ticker, start=start_date, end=end_date)
    if "Close" not in df or df.empty:
        return pd.Series()
    return df["Close"].dropna().sort_index()

def simulate_trade(entry_price, exit_price, signal):
    if entry_price is None or exit_price is None:
        return None
    if signal == "LONG":
        return (exit_price - entry_price) / entry_price
    elif signal == "SHORT":
        return (entry_price - exit_price) / entry_price
    return 0

def run_backtest():
    if not os.path.exists(SIGNAL_FILE):
        print("❌ Signal file not found.")
        return

    signals = pd.read_csv(SIGNAL_FILE)
    signals["date"] = datetime.utcnow().strftime("%Y-%m-%d")

    all_results = []

    for _, row in signals.iterrows():
        pair = row["pair"]
        signal = row["signal"]
        yf_ticker = PAIR_TO_YF.get(pair)

        if not yf_ticker or signal == "NEUTRAL":
            continue

        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=PRICE_LOOKBACK_DAYS)
        hold_end_date = end_date + timedelta(days=HOLD_PERIOD_DAYS)

        prices = fetch_price_data(yf_ticker, start_date.strftime("%Y-%m-%d"), hold_end_date.strftime("%Y-%m-%d"))
        if len(prices) < HOLD_PERIOD_DAYS + 1:
            print(f"⚠️ Not enough data for {pair} — skipping")
            continue

        try:
            entry_price = float(prices.iloc[-HOLD_PERIOD_DAYS - 1])
            exit_price = float(prices.iloc[-1])
        except Exception as e:
            print(f"⚠️ Error extracting prices for {pair}: {e}")
            continue

        return_pct = simulate_trade(entry_price, exit_price, signal)
        if return_pct is None:
            print(f"⚠️ Invalid return for {pair} — skipping")
            continue

        all_results.append({
            "pair": pair,
            "signal": signal,
            "entry_price": round(entry_price, 5),
            "exit_price": round(exit_price, 5),
            "return_pct": round(return_pct * 100, 2)
        })

    if not all_results:
        print("⚠️ No valid trades found — check signal content and yfinance data.")
        return

    results_df = pd.DataFrame(all_results)
    results_df["return_pct"] = pd.to_numeric(results_df["return_pct"], errors="coerce")
    results_df.dropna(subset=["return_pct"], inplace=True)

    results_df.to_csv("data/backtest_results.csv", index=False)

    total_return = results_df["return_pct"].sum()
    avg_return = results_df["return_pct"].mean()
    win_rate = (results_df["return_pct"] > 0).mean() * 100

    print(f"\n📊 Backtest Summary")
    print(f"------------------")
    print(f"Total Trades  : {len(results_df)}")
    print(f"Win Rate      : {win_rate:.2f}%")
    print(f"Avg Return    : {avg_return:.2f}%")
    print(f"Total Return  : {total_return:.2f}%")

if __name__ == "__main__":
    run_backtest()
