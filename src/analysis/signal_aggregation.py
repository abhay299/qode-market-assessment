import os
import math
import joblib
import numpy as np
import pandas as pd
from utils.logger import get_logger

logger = get_logger("signal_aggregation")

VECTORS_PATH = "data/outputs/tfidf_vectors.joblib"
PARQUET_PATH = "data/processed/tweets.parquet"


def aggregate_market_signal():
    if not os.path.exists(VECTORS_PATH):
        logger.error("TF-IDF vectors not found")
        return

    if not os.path.exists(PARQUET_PATH):
        logger.error("Tweets parquet not found")
        return

    # Load data
    tfidf_matrix = joblib.load(VECTORS_PATH)
    df = pd.read_parquet(PARQUET_PATH)

    # --- Tweet-level signal ---
    # L2 norm of TF-IDF vector
    tweet_signals = np.linalg.norm(tfidf_matrix.toarray(), axis=1)

    df["tweet_signal"] = tweet_signals

    # --- Market-level aggregation ---
    mean_signal = tweet_signals.mean()
    std_signal = tweet_signals.std(ddof=1)
    n = len(tweet_signals)

    standard_error = std_signal / math.sqrt(n)

    confidence_interval = (
        mean_signal - 1.96 * standard_error,
        mean_signal + 1.96 * standard_error,
    )

    logger.info(f"Market signal mean: {mean_signal:.4f}")
    logger.info(f"95% CI: {confidence_interval}")

    print("\n📈 Market-Level Signal")
    print(f"Number of tweets: {n}")
    print(f"Mean signal: {mean_signal:.4f}")
    print(f"95% confidence interval: {confidence_interval}")

    return {
        "n_tweets": n,
        "mean_signal": mean_signal,
        "confidence_interval": confidence_interval,
    }
