import requests
import json
import os
from datetime import datetime

# Create data directory if not exists
os.makedirs("data", exist_ok=True)

# NewsAPI configuration
API_KEY = "03119f5cab234976979f11bf44ed800c"
URL = "https://newsapi.org/v2/everything"

# Currency keywords to track
CURRENCY_KEYWORDS = ["EUR/USD", "USD/JPY", "GBP/USD", "EUR", "USD", "JPY", "GBP", "forex", "interest rate", "FOMC", "ECB", "BoJ", "BoE"]

# Fetch and store FX news
def fetch_fx_news():
    query = " OR ".join(CURRENCY_KEYWORDS)
    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 100,
        "apiKey": API_KEY
    }
    response = requests.get(URL, params=params)
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        output_path = f"data/raw_fx_news_{timestamp}.json"
        with open(output_path, "w") as f:
            json.dump(articles, f, indent=2)
        print(f"✅ Saved {len(articles)} articles to {output_path}")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    fetch_fx_news()
