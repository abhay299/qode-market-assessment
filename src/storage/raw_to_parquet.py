import json
import os
import pandas as pd
from utils.logger import get_logger

logger = get_logger("raw_to_parquet")

RAW_PATH = "data/raw/tweets_raw.jsonl"
OUTPUT_PATH = "data/processed/tweets.parquet"


def jsonl_to_parquet():
    if not os.path.exists(RAW_PATH):
        logger.error("Raw data file does not exist")
        return

    os.makedirs("data/processed", exist_ok=True)

    records = []

    with open(RAW_PATH, "r", encoding="utf-8") as f:
        for line in f:
            try:
                record = json.loads(line)
                records.append(record)
            except json.JSONDecodeError:
                continue

    if not records:
        logger.warning("No records found in raw file")
        return

    df = pd.DataFrame(records)

    # Ensure column order (stable schema)
    df = df[
        [
            "tweet_id",
            "username",
            "timestamp",
            "content",
            "hashtags",
            "mentions",
            "language",
            "likes",
            "retweets",
            "replies",
        ]
    ]

    df.to_parquet(OUTPUT_PATH, index=False)

    logger.info(f"Saved {len(df)} records to {OUTPUT_PATH}")
    print(f"Parquet file created: {OUTPUT_PATH}")
