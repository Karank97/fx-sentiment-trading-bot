import re
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax

MODEL_NAME = "ProsusAI/finbert"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME).to(device)
label_map = {0: "negative", 1: "neutral", 2: "positive"}

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    return text.strip()

def predict_sentiment(title, description):
    text = clean_text(f"{title} {description}")
    inputs = tokenizer(text, return_tensors="pt", truncation=True).to(device)
    with torch.no_grad():
        outputs = model(**inputs)
    probs = softmax(outputs.logits.cpu().numpy()[0])
    label_idx = probs.argmax()
    label = label_map[label_idx]
    confidence = float(probs[label_idx])
    return {"label": label, "confidence": round(confidence, 4)}

if __name__ == "__main__":
    # Example usage
    title = "USD rallies as Fed signals aggressive rate hike"
    description = "The dollar strengthened after the Federal Reserve hinted at a steeper tightening path."
    result = predict_sentiment(title, description)
    print(f"🧠 Prediction: {result['label']} (confidence: {result['confidence']})")
