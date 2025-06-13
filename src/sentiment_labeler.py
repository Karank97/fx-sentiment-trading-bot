import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax

INPUT_FILE = "data/cleaned_fx_news.csv"
OUTPUT_FILE = "data/labeled_fx_news.csv"

MODEL_NAME = "ProsusAI/finbert"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME).to(device)
label_map = {0: "negative", 1: "neutral", 2: "positive"}

def predict_finbert(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True).to(device)
    with torch.no_grad():
        outputs = model(**inputs)
    probs = softmax(outputs.logits.cpu().numpy()[0])
    label_idx = probs.argmax()
    return label_map[label_idx], float(probs[label_idx])

def label_sentiment():
    df = pd.read_csv(INPUT_FILE)
    rows = []

    for _, row in df.iterrows():
        combined_text = f"{row['title']} {row['description']}"
        label, confidence = predict_finbert(combined_text)

        rows.append({
            "title": row["title"],
            "description": row["description"],
            "source": row["source"],
            "publishedAt": row["publishedAt"],
            "confidence": round(confidence, 4),
            "label": label
        })

    labeled_df = pd.DataFrame(rows)
    labeled_df.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ FinBERT-labeled data saved to {OUTPUT_FILE} — {len(labeled_df)} entries")

if __name__ == "__main__":
    label_sentiment()
