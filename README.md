# 💹 FX Sentiment Trading Bot

A real-time machine learning pipeline that converts financial news sentiment into trading signals for major currency pairs (e.g., EUR/USD, USD/JPY).  
This project combines NLP, FinBERT, trading logic, and a Streamlit dashboard to simulate and visualize trading based on macroeconomic sentiment.

[![Python](https://img.shields.io/badge/Built_with-Python-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-ff4b4b)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Made With Python](https://img.shields.io/badge/Made%20with-Python%203.10-blue)
![FinBERT](https://img.shields.io/badge/NLP-FinBERT-yellow)
![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-red)
![Status](https://img.shields.io/badge/Status-In_Progress-orange)

---

## 📌 Project Overview

This project explores whether machine-learned sentiment from FX headlines can be used to generate trading signals.  
Inspired by macro-trading strategies, the bot performs a complete NLP + trading pipeline using FinBERT:

- Scrape FX news headlines
- Clean and label sentiment with FinBERT
- Generate real-time trade signals (LONG/SHORT/NEUTRAL)
- Log predictions and backtest the strategy
- Visualize everything in a live dashboard

---

## 🧠 Features

- ✅ **FinBERT Sentiment Labeling**: Directly applies pre-trained FinBERT for FX sentiment
- ✅ **Live Signal Generator**: Predicts sentiment and maps it to FX pair signals
- ✅ **Backtesting Engine**: Measures return %, win rate, and Sharpe ratio
- ✅ **Streamlit Dashboard**: Real-time visual display of all logged signals
- ✅ **Modular Design**: Easily extensible with custom indicators or trading APIs

---

## 🖥️ How to Run It

### 1. Clone + Setup Environment

```bash
git clone https://github.com/Karank97/fx-sentiment-trading-bot.git
cd fx-sentiment-trading-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
2. Run the Full Pipeline
bash
Copy
Edit
# Run full pipeline (in order)
python3 src/core/data_pipeline.py
python3 src/nlp/clean_news.py
python3 src/nlp/inference.py
python3 src/core/signal_generator.py
python3 src/core/backtest_signals.py
3. Launch Streamlit Dashboard
bash
Copy
Edit
streamlit run dashboard/app.py
Then visit: http://localhost:8501

📊 Example Signal Output
bash
Copy
Edit
📈 Signal: LONG EUR/USD | Sentiment: bullish | Confidence: 0.89
📉 Signal: SHORT USD/JPY | Sentiment: bearish | Confidence: 0.76
🧰 Tech Stack
Python 3.10

FinBERT – Sentiment classification

Scikit-learn – Evaluation tools

YFinance – FX price data

Streamlit – Dashboard

Joblib – Model persistence

Pandas – Data wrangling

📁 Project Structure
bash
Copy
Edit
fx-sentiment-trading-bot/
│
├── data/                 # Raw, cleaned, labeled, and backtest CSVs
├── src/
│   ├── core/             # Pipeline: fetch, backtest, signal, returns
│   ├── live/             # Automated signal loops
│   ├── nlp/              # Clean + label FX news sentiment
│   └── utils/            # Helper utilities
├── dashboard/            # Streamlit UI app
├── scripts/              # CLI tools (e.g., backfill, clean logs)
├── requirements.txt
└── README.md
🚧 Future Improvements
📈 Add cumulative PnL + drawdown to dashboard

🔄 Automate signal loop with CRON scheduler

💸 Integrate OANDA or Alpaca for paper/live trading

📤 Add Telegram or email alerts for signals

📜 License
This project is licensed under the MIT License.