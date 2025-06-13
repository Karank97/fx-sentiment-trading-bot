# src/live_signal_generator.py

import pandas as pd
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from scipy.special import softmax
from datetime import datetime

# Load FinBERT
MODEL_NAME = "yiyanghkust/finbert-tone"
tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
model = BertForSequenceClassification.from_pretrained(MODEL_NAME)

# Define mapping from sentiment to FX signals
def sentiment_to_signal(sentiment):
    if sentiment == "positive":
        return "LONG EUR/USD"
    elif sentiment == "negative":
        return "SHORT USD/JPY"
    else:
        return "NEUTRAL"

# Prediction function
def finbert_predict(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    probs = softmax(outputs.logits.numpy()[0])
    labels = ["negative", "neutral", "positive"]
    idx = probs.argmax()
    return labels[idx], float(probs[idx])

# Load cleaned news
df = pd.read_csv("data/cleaned_fx_news.csv")
latest = df.iloc[-1]
text = f"{latest['title']} {latest['description']}"
timestamp = datetime.utcnow().isoformat()

# Run prediction
sentiment, confidence = finbert_predict(text)
signal = sentiment_to_signal(sentiment)

# Log result
log_data = {
    "timestamp": [timestamp],
    "pair": [signal.split()[-1]],
    "headline": [text],
    "label": [sentiment],
    "confidence": [confidence],
    "signal": [signal]
}
log_df = pd.DataFrame(log_data)
log_df.to_csv("data/live_signals_log.csv", mode="a", index=False, header=not pd.io.common.file_exists("data/live_signals_log.csv"))

print(f"📈 Signal: {signal} | Sentiment: {sentiment} | Confidence: {confidence:.4f}")
print(f"📝 Logged 1 signal(s) to data/live_signals_log.csv")
