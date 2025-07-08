import os
import json
import pandas as pd
import re

RAW_DATA_DIR = "data/"
CLEANED_FILE = "data/cleaned_fx_news.csv"

FX_KEYWORDS = [
    "forex", "currency", "central bank", "rate hike", "rate cut", "inflation", "interest rate",
    "dollar", "euro", "yen", "pound", "usd", "eur", "jpy", "gbp", "market", "bond", "fed", "ecb", "boj", "boe"
]

def clean_text(text):
    if not text:
        return ""
    text = re.sub(r"http\\S+", "", text)
    text = re.sub(r"[^a-zA-Z\\s]", "", text)
    text = text.lower().strip()
    return text

def is_fx_related(text):
    text = text.lower()
    return any(keyword in text for keyword in FX_KEYWORDS)

def process_news_files():
    cleaned_rows = []
    for filename in os.listdir(RAW_DATA_DIR):
        if filename.startswith("raw_fx_news") and filename.endswith(".json"):
            with open(os.path.join(RAW_DATA_DIR, filename), "r") as f:
                articles = json.load(f)
                for article in articles:
                    title = clean_text(article.get("title", ""))
                    description = clean_text(article.get("description", ""))
                    combined = f"{title} {description}"
                    if is_fx_related(combined):
                        cleaned_rows.append({
                            "title": title,
                            "description": description,
                            "source": article.get("source", {}).get("name", ""),
                            "publishedAt": article.get("publishedAt", "")
                        })

    df = pd.DataFrame(cleaned_rows)
    df.to_csv(CLEANED_FILE, index=False)
    print(f"✅ Saved filtered FX data to {CLEANED_FILE} — {len(df)} entries")

if __name__ == "__main__":
    process_news_files()
