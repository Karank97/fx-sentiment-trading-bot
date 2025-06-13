import time
import pandas as pd
from data_pipeline import fetch_fx_news
from clean_news import process_news_files
from sentiment_labeler import label_sentiment
from live_signal_generator import generate_trade_signal, log_signals

NEWS_LIMIT = 100
LOOP_DELAY = 600  # 10 minutes

def run_pipeline_once():
    print("🕵️ Fetching FX news...")
    fetch_fx_news()

    print("🧹 Cleaning news...")
    process_news_files()

    print("🧠 Labeling sentiment with FinBERT...")
    label_sentiment()

    print("📈 Generating trade signals...")
    df = pd.read_csv("data/labeled_fx_news.csv").tail(NEWS_LIMIT)
    all_signals = []

    for _, row in df.iterrows():
        title = row["title"]
        description = row["description"]
        predictions = generate_trade_signal(title, description)
        all_signals.extend(predictions)

    if all_signals:
        log_signals(all_signals)
        print(f"✅ Logged {len(all_signals)} signal(s).\n")
    else:
        print("⚠️ No signals generated.\n")

if __name__ == "__main__":
    print("🚀 Auto loop started (CTRL+C to stop)")
    try:
        while True:
            run_pipeline_once()
            print(f"⏳ Sleeping for {LOOP_DELAY // 60} minutes...\n")
            time.sleep(LOOP_DELAY)
    except KeyboardInterrupt:
        print("🛑 Auto loop manually stopped.")
