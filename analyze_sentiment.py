"""
analyze_sentiment.py
Runs VADER sentiment analysis (a well-established, free NLP tool built for exactly
this kind of short-text sentiment scoring) on each headline, then groups and
summarizes the results in plain English.

This is the legitimate way to describe this piece: "applies an established NLP
sentiment model to a live data pipeline" -- not "trained a new machine learning
model." Both are real engineering, but be precise about which one this is.
"""

import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def classify(headline_text):
    scores = analyzer.polarity_scores(headline_text)
    compound = scores["compound"]
    if compound >= 0.05:
        label = "positive"
    elif compound <= -0.05:
        label = "negative"
    else:
        label = "neutral"
    return label, compound


def plain_english_summary(label, count, total):
    if label == "positive":
        return f"{count} of {total} headlines lean positive today."
    elif label == "negative":
        return f"{count} of {total} headlines lean negative today."
    else:
        return f"{count} of {total} headlines are neutral/mixed today."


def analyze(headlines):
    results = []
    counts = {"positive": 0, "negative": 0, "neutral": 0}

    for h in headlines:
        label, score = classify(h["title"])
        counts[label] += 1
        results.append({**h, "sentiment": label, "score": round(score, 3)})

    total = len(headlines)
    overall = max(counts, key=counts.get) if total > 0 else "neutral"

    summary_lines = [plain_english_summary(lbl, cnt, total) for lbl, cnt in counts.items() if cnt > 0]

    return {
        "overall_tone": overall,
        "counts": counts,
        "summary_lines": summary_lines,
        "headlines": results,
    }


if __name__ == "__main__":
    with open("headlines.json") as f:
        data = json.load(f)

    analysis = analyze(data["headlines"])
    analysis["fetched_at"] = data["fetched_at"]

    with open("analysis.json", "w") as f:
        json.dump(analysis, f, indent=2)

    print(f"Overall tone: {analysis['overall_tone']}")
    for line in analysis["summary_lines"]:
        print(" -", line)
