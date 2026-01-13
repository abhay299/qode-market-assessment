import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from processing.text_cleaner import clean_text
from utils.logger import get_logger
import joblib

logger = get_logger("tfidf_signal")

PARQUET_PATH = "data/processed/tweets.parquet"
OUTPUT_DIR = "data/outputs"
VECTORS_PATH = f"{OUTPUT_DIR}/tfidf_vectors.joblib"
FEATURES_PATH = f"{OUTPUT_DIR}/tfidf_features.joblib"


def generate_tfidf_signals(max_features: int = 500):
    if not os.path.exists(PARQUET_PATH):
        logger.error("Parquet file not found")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = pd.read_parquet(PARQUET_PATH)

    # Clean content
    df["clean_text"] = df["content"].apply(clean_text)

    texts = df["clean_text"].tolist()

    vectorizer = TfidfVectorizer(
        max_features=max_features,
        stop_words="english",
        ngram_range=(1, 2),
    )

    tfidf_matrix = vectorizer.fit_transform(texts)

    # Persist for reuse (memory efficient)
    joblib.dump(tfidf_matrix, VECTORS_PATH)
    joblib.dump(vectorizer.get_feature_names_out(), FEATURES_PATH)

    logger.info(
        f"TF-IDF generated: {tfidf_matrix.shape[0]} rows × {tfidf_matrix.shape[1]} features"
    )

    print(
        f"TF-IDF complete → shape = {tfidf_matrix.shape}, features saved"
    )
