import pandas as pd
import re
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib

INPUT_FILE = "data/labeled_fx_news.csv"
MODEL_FILE = "models/random_forest_model.pkl"
VECTORIZER_FILE = "models/tfidf_vectorizer.pkl"

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    return text.strip()

def train_model():
    if not os.path.exists(INPUT_FILE):
        print("❌ Labeled data not found.")
        return

    df = pd.read_csv(INPUT_FILE)
    df["text"] = (df["title"].fillna("") + " " + df["description"].fillna("")).apply(clean_text)

    X = df["text"]
    y = df["label"]

    vectorizer = TfidfVectorizer(max_features=3000)
    X_vectorized = vectorizer.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_vectorized, y, test_size=0.2, random_state=42)

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)

    print("📊 Classification Report:")
    print(classification_report(y_test, y_pred))
    print("🧮 Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    os.makedirs("models", exist_ok=True)
    joblib.dump(clf, MODEL_FILE)
    joblib.dump(vectorizer, VECTORIZER_FILE)

    print(f"✅ Model saved to {MODEL_FILE}")
    print(f"✅ Vectorizer saved to {VECTORIZER_FILE}")

if __name__ == "__main__":
    train_model()
