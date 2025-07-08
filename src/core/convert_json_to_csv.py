import json
import pandas as pd
import os
import glob

INPUT_FOLDER = "data"
OUTPUT_CSV = "data/raw_news.csv"

def convert_all_json_to_csv():
    json_files = glob.glob(os.path.join(INPUT_FOLDER, "raw_fx_news_*.json"))
    all_articles = []

    print(f"🔍 Found {len(json_files)} JSON files.")

    for file in sorted(json_files):
        with open(file, "r") as f:
            try:
                articles = json.load(f)
                for article in articles:
                    title = article.get("title", "")
                    description = article.get("description", "")
                    timestamp = article.get("publishedAt", "")
                    if title or description:
                        all_articles.append({
                            "timestamp": timestamp,
                            "title": title,
                            "description": description
                        })
            except json.JSONDecodeError:
                print(f"⚠️ Skipping malformed JSON file: {file}")

    if not all_articles:
        print("❌ No valid articles found.")
        return

    df = pd.DataFrame(all_articles)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"✅ Combined {len(df)} articles → {OUTPUT_CSV}")

if __name__ == "__main__":
    convert_all_json_to_csv()
