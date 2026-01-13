# from scraper.x_scraper import XScraper
# from utils.logger import get_logger

# logger = get_logger("main")

# def main():
#     logger.info("Step A (Nitter): Detecting tweet elements")

#     scraper = XScraper()
#     scraper.detect_tweets()
#     scraper.close()

#     logger.info("Step A completed")

# if __name__ == "__main__":
#     main()

from scraper.x_scraper import XScraper
from storage.raw_to_parquet import jsonl_to_parquet
from analysis.tfidf_signal import generate_tfidf_signals
from analysis.signal_aggregation import aggregate_market_signal
from visualization.market_signal_plot import plot_market_signal
from utils.logger import get_logger

logger = get_logger("pipeline")


def run_pipeline():
    logger.info("🚀 Starting full market intelligence pipeline")

    # ---- Step 1: Scrape tweets ----
    logger.info("Step 1: Scraping tweets")
    scraper = XScraper()
    scraper.detect_tweets()
    scraper.close()

    # ---- Step 2: Raw → Parquet ----
    logger.info("Step 2: Converting raw data to Parquet")
    jsonl_to_parquet()

    # ---- Step 3: TF-IDF signals ----
    logger.info("Step 3: Generating TF-IDF signals")
    generate_tfidf_signals()

    # ---- Step 4: Market-level aggregation ----
    logger.info("Step 4: Aggregating market signal")
    aggregate_market_signal()

    # ---- Step 5: Visualization ----
    logger.info("Step 5: Visualizing market signal")
    plot_market_signal()

    logger.info("✅ Pipeline completed successfully")


if __name__ == "__main__":
    run_pipeline()
