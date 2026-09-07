"""
generate_site.py
Turns analysis.json into a clean, readable static index.html page.
"""

import json
from datetime import datetime

TONE_COLORS = {"positive": "#1a7f37", "negative": "#c53030", "neutral": "#666666"}
TONE_EMOJI = {"positive": "up", "negative": "down", "neutral": "flat"}

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Daily Market Sentiment Digest</title>
<style>
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    max-width: 700px;
    margin: 40px auto;
    padding: 0 20px;
    color: #1a1a1a;
    line-height: 1.5;
  }}
  h1 {{ font-size: 1.6rem; margin-bottom: 0; }}
  .date {{ color: #666; font-size: 0.9rem; margin-bottom: 24px; }}
  .tone-banner {{
    padding: 14px 18px;
    border-radius: 8px;
    background: #f5f5f5;
    border-left: 4px solid {tone_color};
    margin-bottom: 24px;
    font-size: 1.05rem;
  }}
  .headline {{
    padding: 12px 0;
    border-bottom: 1px solid #eee;
  }}
  .headline a {{
    color: #1a1a1a;
    text-decoration: none;
    font-weight: 500;
  }}
  .headline a:hover {{ text-decoration: underline; }}
  .meta {{
    font-size: 0.8rem;
    color: #888;
    margin-top: 4px;
  }}
  .tag {{
    display: inline-block;
    padding: 2px 8px;
    border-radius: 10px;
    font-size: 0.75rem;
    font-weight: 600;
    color: white;
  }}
  footer {{ margin-top: 40px; font-size: 0.8rem; color: #999; }}
</style>
</head>
<body>
  <h1>Daily Market Sentiment Digest</h1>
  <div class="date">{date}</div>

  <div class="tone-banner">
    Today's overall tone: <strong>{overall_tone}</strong><br>
    {summary_lines_html}
  </div>

  <div class="headlines">
    {headlines_html}
  </div>

  <footer>
    Built by Shanyu Tiwari. Headline sentiment scored using VADER, an established
    open-source sentiment analysis tool. This is informational only, not financial advice.
  </footer>
</body>
</html>
"""

HEADLINE_TEMPLATE = """
<div class="headline">
  <a href="{url}" target="_blank">{title}</a>
  <span class="tag" style="background:{color}">{sentiment}</span>
  <div class="meta">{source}</div>
</div>
"""


def generate():
    with open("analysis.json") as f:
        analysis = json.load(f)

    headlines_html = "\n".join(
        HEADLINE_TEMPLATE.format(
            url=h["url"],
            title=h["title"],
            sentiment=h["sentiment"],
            color=TONE_COLORS[h["sentiment"]],
            source=h["source"],
        )
        for h in analysis["headlines"]
    )

    summary_lines_html = "<br>".join(analysis["summary_lines"])

    html = HTML_TEMPLATE.format(
        date=datetime.utcnow().strftime("%B %d, %Y"),
        overall_tone=analysis["overall_tone"].upper(),
        tone_color=TONE_COLORS[analysis["overall_tone"]],
        summary_lines_html=summary_lines_html,
        headlines_html=headlines_html,
    )

    with open("index.html", "w") as f:
        f.write(html)

    print("Generated index.html")


if __name__ == "__main__":
    generate()
