import os
import math
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils.logger import get_logger

logger = get_logger("market_signal_plot")

VECTORS_PATH = "data/outputs/tfidf_vectors.joblib"
PARQUET_PATH = "data/processed/tweets.parquet"

def plot_market_signal(sample_size: int = 500):
    if not os.path.exists(VECTORS_PATH) or not os.path.exists(PARQUET_PATH):
        logger.error("Required files not found")
        return

    tfidf_matrix = joblib.load(VECTORS_PATH)
    tweet_signals = np.linalg.norm(tfidf_matrix.toarray(), axis=1)

    # Optional downsampling
    if len(tweet_signals) > sample_size:
        tweet_signals = np.random.choice(
            tweet_signals, size=sample_size, replace=False
        )

    unique_vals = np.unique(tweet_signals)

    mean_signal = tweet_signals.mean()
    std_signal = tweet_signals.std(ddof=1)
    n = len(tweet_signals)
    stderr = std_signal / math.sqrt(n) if n > 1 else 0.0

    ci_low = mean_signal - 1.96 * stderr
    ci_high = mean_signal + 1.96 * stderr

    print("\n📊 Market Signal Summary")
    print(f"Number of tweets: {n}")
    print(f"Mean signal: {mean_signal:.4f}")
    print(f"95% CI: ({ci_low}, {ci_high})")

    # ---- If no variance, skip plotting ----
    if len(unique_vals) < 2:
        print("⚠️ All tweet signals identical — skipping histogram visualization.")
        return

    # ---- Plot only if meaningful ----
    num_bins = min(30, len(unique_vals))

    plt.figure(figsize=(8, 4))
    plt.hist(tweet_signals, bins=num_bins, alpha=0.7)
    plt.axvline(mean_signal)
    plt.axvline(ci_low)
    plt.axvline(ci_high)

    plt.title("Market Signal Distribution (TF-IDF Intensity)")
    plt.xlabel("Tweet-level Signal Strength")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()
