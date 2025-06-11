import joblib
import pandas as pd
import re
import os

MODEL_PATH = "models/random_forest_model.pkl"
VECTORIZER_PATH = "models/tfidf_vectorizer.pkl"

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    return text.strip()

def load_model():
    if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
        raise FileNotFoundError("Model or vectorizer not found. Run train_random_forest.py first.")
    clf = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    return clf, vectorizer

def predict_sentiment(title, description):
    clf, vectorizer = load_model()
    text = clean_text(f"{title} {description}")
    X = vectorizer.transform([text])
    label = clf.predict(X)[0]
    proba = clf.predict_proba(X).max()
    return {"label": label, "confidence": round(proba, 4)}

if __name__ == "__main__":
    # Example usage
    title = "USD surges as Fed hints at aggressive rate hike"
    description = "The dollar strengthened significantly after the Federal Reserve signaled more rate increases ahead."

    result = predict_sentiment(title, description)
    print(f"🧠 Prediction: {result['label']} (confidence: {result['confidence']})")
