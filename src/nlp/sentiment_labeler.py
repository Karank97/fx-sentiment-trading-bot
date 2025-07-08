import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax

INPUT_FILE = "data/cleaned_fx_news.csv"
OUTPUT_FILE = "data/labeled_fx_news.csv"
BATCH_SIZE = 16

MODEL_NAME = "ProsusAI/finbert"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME).to(device)
label_map = {0: "negative", 1: "neutral", 2: "positive"}


def batched_predict(texts):
    inputs = tokenizer(
        texts,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=512
    ).to(device)

    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits.cpu().numpy()
    probs = softmax(logits, axis=1)
    labels = probs.argmax(axis=1)
    confidences = probs.max(axis=1)

    return [label_map[i] for i in labels], confidences.tolist()


def label_sentiment():
    df = pd.read_csv(INPUT_FILE)
    texts = (df["title"].fillna("") + " " + df["description"].fillna("")).tolist()

    all_labels = []
    all_confidences = []

    for i in range(0, len(texts), BATCH_SIZE):
        batch_texts = texts[i:i + BATCH_SIZE]
        try:
            labels, confidences = batched_predict(batch_texts)
        except Exception as e:
            print(f"⚠️ Batch failed at index {i}: {e}")
            labels = ["neutral"] * len(batch_texts)
            confidences = [0.0] * len(batch_texts)

        all_labels.extend(labels)
        all_confidences.extend([round(c, 4) for c in confidences])
        print(f"✅ Processed {min(i + BATCH_SIZE, len(texts))} / {len(texts)}")

    df["label"] = all_labels
    df["confidence"] = all_confidences

    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\n✅ FinBERT-labeled data saved to {OUTPUT_FILE} — {len(df)} entries")


if __name__ == "__main__":
    label_sentiment()
