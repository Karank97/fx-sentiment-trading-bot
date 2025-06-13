# 💹 FX Sentiment Trading Bot

A real-time machine learning pipeline that converts financial news sentiment into trading signals for major currency pairs (e.g., EUR/USD, USD/JPY).  
This project uses FinBERT for sentiment classification and maps signals to live trade directions with a Streamlit dashboard for visualization.

[![Python](https://img.shields.io/badge/Built_with-Python-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-ff4b4b)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📌 Project Overview

This bot explores whether real-time sentiment from FX news can generate statistically meaningful trading signals. Inspired by macro-trading strategies and sentiment-driven volatility, this pipeline does the following:

- Scrapes FX news headlines
- Cleans and filters for relevant financial news
- Labels sentiment using **FinBERT**, a transformer model for financial text
- Maps sentiment to LONG / SHORT / NEUTRAL signals for currency pairs
- Logs signals and backtests them against historical FX price data
- Visualizes all signals via a live Streamlit dashboard

---

## 🧠 Features

- ✅ **FinBERT Sentiment Classifier**: Transformer-based financial NLP
- ✅ **Real-Time Signal Generator**: Converts sentiment to FX trading direction
- ✅ **Backtesting Engine**: Measures return %, win rate, and Sharpe ratio
- ✅ **Streamlit Dashboard**: Interactive UI to view and filter logged signals
- ✅ **Auto Signal Loop**: Optional cron job or scheduled loop to auto-pull headlines every 10 mins

---

## 🖥️ How to Run It

### 1. Clone + Set Up Environment

```bash
git clone https://github.com/Karank97/fx-sentiment-trading-bot.git
cd fx-sentiment-trading-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
````

### 2. Run the Full Pipeline

```bash
python3 src/data_pipeline.py            # Download fresh FX news
python3 src/clean_news.py               # Filter relevant FX headlines
python3 src/sentiment_labeler.py        # (optional: VADER only — default is FinBERT)
python3 src/inference.py                # Run FinBERT prediction on latest news
python3 src/live_signal_generator.py    # Generate trade signals from labeled news
python3 src/backtest_signals.py         # Backtest signal performance
```

### 3. Launch Streamlit Dashboard

```bash
streamlit run dashboard/app.py
```

Then go to: [http://localhost:8501](http://localhost:8501)

---

## 🔁 Optional: Run Signal Loop Automatically

```bash
python3 src/auto_signal_loop.py
```

To run this every 10 minutes as a background job, set up a cron job like:

```bash
*/10 * * * * cd /Users/karan/Documents/fx-sentiment-trading-bot && /Users/karan/Documents/fx-sentiment-trading-bot/venv/bin/python3 src/auto_signal_loop.py >> cron_log.txt 2>&1
```

---

## 📊 Example Output

```bash
🧠 Prediction: positive (confidence: 0.88)
📈 Signal: LONG EUR/USD | Sentiment: positive | Confidence: 0.88
📝 Logged 1 signal(s) to data/live_signals_log.csv
```

---

## 🧰 Tech Stack

* **Python 3.10**
* **FinBERT** – Transformer-based financial sentiment model
* **Huggingface Transformers** – Model hosting and inference
* **YFinance** – FX price data
* **Streamlit** – Dashboard and live visualization
* **Pandas** – Data wrangling
* **Cron (optional)** – For background signal automation

---

## 📁 Project Structure

```
fx-sentiment-trading-bot/
│
├── data/                 # Raw, cleaned, labeled, and logged data
├── src/                  # Source code
│   ├── data_pipeline.py
│   ├── clean_news.py
│   ├── inference.py
│   ├── live_signal_generator.py
│   ├── auto_signal_loop.py
│   └── backtest_signals.py
├── dashboard/            # Streamlit dashboard
│   └── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚧 Future Improvements

* 📉 Add risk-adjusted performance metrics (Sharpe ratio, max drawdown)
* 🧠 Fine-tune FinBERT on FX-specific labeled data
* 💹 Integrate live trading via OANDA/Alpaca API
* 🔔 Add Telegram or email alerts for new signals
* 📊 Visualize rolling returns, PnL, and drawdowns in dashboard

---

## 📜 License

This project is licensed under the MIT License – see [LICENSE] for details.


