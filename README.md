# 💹 FX Sentiment Trading Bot

A real-time machine learning pipeline that converts financial news sentiment into trading signals for major currency pairs (e.g., EUR/USD, USD/JPY).  
This project combines NLP, classification models, trading logic, and a Streamlit dashboard to simulate and visualize trading based on macroeconomic sentiment.

[![Python](https://img.shields.io/badge/Built_with-Python-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-ff4b4b)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📌 Project Overview

This project was built to explore whether machine-learned sentiment from FX headlines can be used to generate better-than-random trade signals. Inspired by the rise of social sentiment and macro-trading strategies, the bot performs the full ML + trading cycle:

- Scrape FX news headlines
- Clean and label sentiment using NLP
- Train a sentiment classifier (Random Forest)
- Generate real-time trade signals (LONG/SHORT/NEUTRAL)
- Log predictions and backtest the strategy
- Visualize it all in a live dashboard

---

## 🧠 Features

- ✅ **Sentiment Classifier**: Trained on FX-labeled news using Random Forest + TF-IDF
- ✅ **Live Signal Generator**: Predicts sentiment and maps it to FX pair signals
- ✅ **Backtesting Engine**: Measures return, win rate, drawdown
- ✅ **Streamlit Dashboard**: Real-time visual display of all logged signals
- ✅ **Modular Design**: Easily extensible with LSTM, FinBERT, or live trading APIs

---

## 🖥️ How to Run It

### 1. Clone + Setup Environment

```bash
git clone https://github.com/Karank97/fx-sentiment-trading-bot.git
cd fx-sentiment-trading-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
````

### 2. Run Pipeline Locally

```bash
python3 src/data_pipeline.py              # fetch FX news
python3 src/clean_news.py                 # clean and filter news
python3 src/sentiment_labeler.py          # label sentiment with VADER
python3 src/train_random_forest.py        # train sentiment model
python3 src/live_signal_generator.py      # predict signals and log output
python3 src/backtest_signals.py           # simulate trades on logged signals
```

### 3. Launch Streamlit Dashboard

```bash
streamlit run dashboard/app.py
```

Then open: [http://localhost:8501](http://localhost:8501)

---

## 📊 Example Signal Output

```bash
📈 Signal: LONG EUR/USD | Sentiment: positive | Confidence: 0.89
📈 Signal: SHORT USD/JPY | Sentiment: negative | Confidence: 0.76
```

---

## 🧰 Tech Stack

* **Python 3.10**
* **Scikit-learn** – ML modeling
* **NLTK + VADER** – Sentiment scoring
* **TfidfVectorizer** – Feature engineering
* **YFinance** – FX price data
* **Streamlit** – Dashboard
* **Joblib** – Model persistence
* **Pandas** – Data wrangling

---

## 📁 Project Structure

```
fx-sentiment-trading-bot/
│
├── data/                 # Stored raw, cleaned, labeled, and backtest files
├── models/               # Saved ML model and vectorizer
├── notebooks/            # Jupyter notebooks (optional for dev)
├── src/                  # All functional code modules
│   ├── data_pipeline.py
│   ├── clean_news.py
│   ├── sentiment_labeler.py
│   ├── train_random_forest.py
│   ├── inference.py
│   ├── live_signal_generator.py
│   └── backtest_signals.py
├── dashboard/            # Streamlit UI app
│   └── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚧 Future Improvements

* 🤖 Replace VADER with FinBERT or LSTM for sentiment classification
* 📈 Add cumulative PnL + risk metrics to dashboard
* 🔄 Run live loops with NewsAPI every X minutes
* 💸 Integrate OANDA paper/live trading API
* 📤 Email or Telegram signal alerts

---

## 📜 License

This project is licensed under the MIT License.
