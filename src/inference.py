# src/inference.py

import pandas as pd
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from scipy.special import softmax

# Load FinBERT model + tokenizer
MODEL_NAME = "yiyanghkust/finbert-tone"
tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
model = BertForSequenceClassification.from_pretrained(MODEL_NAME)

def finbert_predict(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    probs = softmax(outputs.logits.numpy()[0])
    labels = ["negative", "neutral", "positive"]
    idx = probs.argmax()
    return labels[idx], float(probs[idx])

# Load most recent news item
df = pd.read_csv("data/cleaned_fx_news.csv")
latest = df.iloc[-1]
combined_text = f"{latest['title']} {latest['description']}"

label, confidence = finbert_predict(combined_text)
print(f"🧠 Prediction: {label} (confidence: {confidence:.4f})")
