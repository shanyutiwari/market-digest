"""
fetch_news.py
Pulls today's top financial/market headlines using the free NewsAPI.org tier.

SETUP:
1. Go to https://newsapi.org/register and sign up for a free API key
   (free tier: 100 requests/day, good enough for one daily pull)
2. Set your key as an environment variable before running:
     export NEWSAPI_KEY="your_key_here"
   (On GitHub Actions, you'll store this as a "repo secret" instead — see workflow file)
"""

import os
import requests
import json
from datetime import datetime

def fetch_headlines(query="stock market OR earnings OR Federal Reserve", max_results=15):
    api_key = os.environ.get("NEWSAPI_KEY")
    if not api_key:
        raise RuntimeError("NEWSAPI_KEY environment variable not set. See setup instructions in this file.")

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": max_results,
        "apiKey": api_key,
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    headlines = []
    for article in data.get("articles", []):
        headlines.append({
            "title": article["title"],
            "source": article["source"]["name"],
            "url": article["url"],
            "publishedAt": article["publishedAt"],
        })
    return headlines


if __name__ == "__main__":
    headlines = fetch_headlines()
    output = {
        "fetched_at": datetime.utcnow().isoformat(),
        "headlines": headlines,
    }
    with open("headlines.json", "w") as f:
        json.dump(output, f, indent=2)
    print(f"Fetched {len(headlines)} headlines -> headlines.json")
