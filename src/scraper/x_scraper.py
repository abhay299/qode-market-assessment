from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from utils.logger import get_logger
import time
import re
import json
import os

logger = get_logger("x_scraper")

RAW_DATA_PATH = "data/raw/tweets_raw.jsonl"
SCRAPE_DELAY_SECONDS = 5 # keep browser open after scraping


class XScraper:
    def __init__(self):
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)

        os.makedirs("data/raw", exist_ok=True)

        logger.info("XScraper initialized (Nitter mode)")

    def _load_existing_ids(self):
        """Load existing tweet_ids from raw storage for deduplication"""
        ids = set()

        if not os.path.exists(RAW_DATA_PATH):
            return ids

        with open(RAW_DATA_PATH, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    record = json.loads(line)
                    if record.get("tweet_id"):
                        ids.add(record["tweet_id"])
                except json.JSONDecodeError:
                    continue

        logger.info(f"Loaded {len(ids)} existing tweet IDs")
        return ids

    def detect_tweets(self):
        url = (
            "https://nitter.net/search?"
            "f=tweets&"
            "q=nifty50&"
            "since=&until=&min_faves="
        )

        logger.info(f"Opening URL: {url}")

        # Open page
        self.driver.get(url)
        time.sleep(3)

        # Refresh once for stability
        logger.info("Refreshing page")
        self.driver.refresh()
        time.sleep(10)

        tweet_elements = self.driver.find_elements(By.CSS_SELECTOR, ".timeline-item")
        logger.info(f"Detected {len(tweet_elements)} tweet elements")

        existing_ids = self._load_existing_ids()
        new_records = []

        for tweet in tweet_elements:
            try:
                # ---------- Username ----------
                username = tweet.find_element(By.CSS_SELECTOR, ".username").text.strip()

                # ---------- Tweet ID ----------
                tweet_link = tweet.find_element(
                    By.CSS_SELECTOR, "a.tweet-link"
                ).get_attribute("href")

                tweet_id = None
                match = re.search(r"/status/(\d+)", tweet_link or "")
                if match:
                    tweet_id = match.group(1)

                if not tweet_id or tweet_id in existing_ids:
                    continue

                # ---------- Timestamp ----------
                timestamp = tweet.find_element(
                    By.CSS_SELECTOR, "span.tweet-date a"
                ).get_attribute("title")

                # ---------- Content ----------
                content = tweet.find_element(
                    By.CSS_SELECTOR, ".tweet-content"
                ).text.strip()

                # ---------- Hashtags & Mentions ----------
                hashtags = re.findall(r"#\w+", content)
                mentions = re.findall(r"@\w+", content)

                tweet_record = {
                    "tweet_id": tweet_id,
                    "username": username,
                    "timestamp": timestamp,
                    "content": content,
                    "hashtags": hashtags or None,
                    "mentions": mentions or None,
                    "language": None,
                    "likes": None,
                    "retweets": None,
                    "replies": None,
                }

                new_records.append(tweet_record)
                existing_ids.add(tweet_id)

            except Exception as e:
                logger.error(f"Error parsing tweet: {e}")

        self._store_raw_records(new_records)

        logger.info(f"Stored {len(new_records)} new tweets to raw storage")
        print(f"Stored {len(new_records)} new tweets to raw storage")

        # Non-blocking delay before closing browser
        logger.info(
            f"Scraping complete. Keeping browser open for {SCRAPE_DELAY_SECONDS} seconds."
        )
        time.sleep(SCRAPE_DELAY_SECONDS)

    def _store_raw_records(self, records):
        if not records:
            logger.info("No new tweets to store")
            return

        with open(RAW_DATA_PATH, "a", encoding="utf-8") as f:
            for record in records:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def close(self):
        logger.info("Closing browser")
        self.driver.quit()
