# 📊 Qode Market Assessment
**End-to-End Market Intelligence Pipeline (Twitter/X – India Markets)**

---

## Overview

This project implements a **fully automated, end-to-end data pipeline** to collect, process, and analyze Indian stock market discussions from Twitter/X using **public data only**.

Due to authentication and login restrictions on X, the project uses **Nitter**, an open‑source alternative frontend, to reliably access public tweets **without paid APIs or brittle login automation**.

The system is designed to:
- Run unattended with a single command
- Be robust under real-world scraping constraints
- Convert text data into quantitative market signals with confidence

---

## Key Highlights

- ✅ No paid APIs
- ✅ No login automation
- ✅ Fully automated pipeline (no manual input)
- ✅ Clean modular architecture
- ✅ Efficient Parquet storage
- ✅ Quantitative signal + confidence interval
- ✅ Lightweight visualization

---

## Architecture

```
Nitter (Public Tweets)
        ↓
Selenium Scraper
        ↓
Raw Storage (JSONL)
        ↓
Deduplication
        ↓
Parquet Storage
        ↓
Text Cleaning
        ↓
TF‑IDF Vectorization
        ↓
Market Signal Aggregation
        ↓
Confidence + Visualization
```

---

## Project Structure (Submission‑Relevant)

```
qode-market-assessment/
├── src/
│   ├── scraper/
│   │   └── x_scraper.py
│   ├── storage/
│   │   └── raw_to_parquet.py
│   ├── processing/
│   │   └── text_cleaner.py
│   ├── analysis/
│   │   ├── tfidf_signal.py
│   │   └── signal_aggregation.py
│   ├── visualization/
│   │   └── market_signal_plot.py
│   ├── utils/
│   │   └── logger.py
│   └── main.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── outputs/
│
├── logs/
├── requirements.txt
└── README.md
```

---

## Tweet Data Model

Each tweet is stored in a structured format:

```json
{
  "tweet_id": "string",
  "username": "@handle",
  "timestamp": "UTC datetime",
  "content": "tweet text",
  "hashtags": ["#nifty50"],
  "mentions": ["@user"],
  "language": null,
  "likes": null,
  "retweets": null,
  "replies": null
}
```

---

## How to Run (Single Command)

### 1️⃣ Create and activate virtual environment

```bash
python -m venv venv
source venv/Scripts/activate
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the entire pipeline

```bash
python src/main.py
```

That’s it.

The pipeline will:
1. Open browser and scrape tweets
2. Store raw data
3. Convert to Parquet
4. Generate TF‑IDF signals
5. Aggregate market signal
6. Display visualization (if meaningful)

No manual input required.

---

## Output Artifacts

After a successful run:

```
data/raw/tweets_raw.jsonl
data/processed/tweets.parquet
data/outputs/tfidf_vectors.joblib
logs/app.log
```

---

## Market Signal Methodology

- **Tweet Signal**: L2 norm of TF‑IDF vector
- **Market Signal**: Mean of tweet signals
- **Uncertainty**: 95% confidence interval using standard error

This provides:
- A single quantitative market‑level signal
- Explicit uncertainty awareness (important for trading systems)

---

## Visualization

- Histogram of tweet‑level signals
- Mean and confidence interval markers
- Automatically skipped if data variance is too low

Designed to be **memory‑safe and numerically robust**.

---

## Engineering Decisions

- Used Nitter to avoid X login walls
- Avoided fragile browser authentication
- JSONL for ingestion, Parquet for analytics
- Modular pipeline with single entry point
- Defensive handling of edge cases

---

## Scalability Notes

The system is designed to scale to 10× data volume using:
- Streaming ingestion
- Columnar storage
- Sampling‑based visualization
- Clear separation of concerns

---

## Conclusion

This project demonstrates a **real‑world, production‑style market intelligence pipeline** that prioritizes robustness, clarity, and analytical rigor over brittle shortcuts.

---

