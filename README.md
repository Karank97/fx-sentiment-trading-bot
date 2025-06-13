# 💹 FX Sentiment Trading Bot

A real-time machine learning pipeline that converts FX news sentiment into trading signals for major currency pairs (e.g., EUR/USD, USD/JPY).  
This project uses NLP (FinBERT), a trained classifier, and a full ML ops loop with signal logging, backtesting, and live dashboards.

[![Python](https://img.shields.io/badge/Built_with-Python-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-ff4b4b)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📌 Project Overview

This bot explores if macro sentiment in FX headlines can generate alpha. It scrapes news, classifies tone with FinBERT, maps it to signals (LONG/SHORT/NEUTRAL), logs predictions, simulates trades, and displays everything on a dashboard.

---

## 🧠 Features

- ✅ **FinBERT Sentiment Classifier** (better FX domain accuracy)
- ✅ **Real-Time Signal Generator** (auto-loop via cron)
- ✅ **Backtesting Engine** (P&L, return %, Sharpe ratio)
- ✅ **Live Dashboard** (Streamlit + Plotly)
- ✅ **Clean Modular Code** (add LSTM, APIs, alerts easily)

---

## 🖥️ How to Run It

### 1. Clone + Setup Environment

```bash
git clone https://github.com/Karank97/fx-sentiment-trading-bot.git
cd fx-sentiment-trading-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
2. Run Inference Pipeline
bash
Copy
Edit
python3 src/data_pipeline.py              # fetch FX news
python3 src/clean_news.py                 # clean and filter news
python3 src/sentiment_labeler.py          # label sentiment using FinBERT
python3 src/live_signal_generator.py      # predict signals and log output
python3 src/backtest_signals.py           # simulate trades on logged signals
3. Launch Streamlit Dashboard
bash
Copy
Edit
streamlit run dashboard/app.py
Then open: http://localhost:8501

🔁 Optional: Auto-Loop with Cron
cron
Copy
Edit
*/10 * * * * cd /path/to/project && /path/to/venv/bin/python3 src/auto_signal_loop.py >> cron_log.txt 2>&1
This runs sentiment + signal prediction every 10 minutes.

📊 Signal Output Example
bash
Copy
Edit
🧠 Prediction: positive (confidence: 0.91)
📈 Signal: LONG GBP/USD | Sentiment: positive | Confidence: 0.91
📁 Project Structure
bash
Copy
Edit
fx-sentiment-trading-bot/
├── data/                 # Cleaned, labeled, and signal logs
├── models/               # ML model + vectorizer
├── src/                  # Code modules
├── dashboard/            # Streamlit UI
├── requirements.txt
└── README.md
🚀 Roadmap
 Add rolling Sharpe + drawdown to dashboard

 Deploy to Streamlit Cloud or HuggingFace Spaces

 Add Telegram/Email signal alerts

 Plug into live paper trading (OANDA API)

📜 License
MIT License — free for commercial or personal use.