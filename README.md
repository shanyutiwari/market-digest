# Daily Market Sentiment Digest

A daily-updating website that pulls financial headlines, scores their sentiment
using an established NLP tool (VADER), and presents a plain-English summary.

## How it works
1. `fetch_news.py` pulls today's top financial headlines from NewsAPI.org
2. `analyze_sentiment.py` scores each headline's sentiment (positive/negative/neutral)
3. `generate_site.py` builds a clean `index.html` page from the results
4. GitHub Actions runs this whole pipeline automatically, once a day, for free

## Setup (do this once)

### 1. Get a free NewsAPI key
Go to https://newsapi.org/register, sign up, and copy your API key.

### 2. Create a GitHub repository
- Go to github.com, click "New repository"
- Name it something like `market-digest`
- Make it **Public** (required for free GitHub Pages)
- Upload all these files to it (or use `git push` if you're comfortable with git)

### 3. Add your API key as a secret
- In your new repo: Settings -> Secrets and variables -> Actions -> New repository secret
- Name: `NEWSAPI_KEY`
- Value: paste your key from step 1

### 4. Turn on GitHub Pages
- In your repo: Settings -> Pages
- Under "Build and deployment," set Source to "Deploy from a branch"
- Select branch `main`, folder `/ (root)`
- Save. Your site will be live at `https://<your-username>.github.io/<repo-name>/`

### 5. Run it for the first time
- Go to the "Actions" tab in your repo
- Click "Daily Market Digest" -> "Run workflow" -> "Run workflow"
- Wait about a minute, then check your GitHub Pages URL

After this, it runs automatically every day at 12:00 UTC and updates the live site.

## Tracking your metrics for college apps
Add a free analytics tool to `generate_site.py`'s HTML template (e.g., a simple
visit counter service) so you have real visitor numbers to cite. Do this before
you start sharing the link so you're not missing early data.

## Known limitation (worth being upfront about)
VADER is a general-purpose sentiment tool, not finance-specific. It sometimes
misreads financial language (e.g., "rate cut" or "flat" don't carry their
everyday-English sentiment in a market context). This is a real, known limitation
worth mentioning honestly in any write-up rather than hiding -- and a natural
"next step" to describe: fine-tuning or using a finance-specific sentiment
lexicon (e.g., Loughran-McDonald) would be the improvement.
