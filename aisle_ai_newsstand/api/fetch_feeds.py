import feedparser
import yaml
import time
from datetime import datetime
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_feeds():
    """Load RSS feed URLs from feeds.yml"""
    try:
        with open('feeds.yml', 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        logger.error(f"Error loading feeds.yml: {e}")
        return []

def fetch_feed(url):
    """Fetch and parse a single RSS feed"""
    try:
        feed = feedparser.parse(url)
        return {
            'title': feed.feed.title,
            'entries': feed.entries,
            'last_updated': datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error fetching feed {url}: {e}")
        return None

def main():
    """Main function to fetch all feeds"""
    feeds = load_feeds()
    if not feeds:
        logger.error("No feeds found in feeds.yml")
        return

    for feed_url in feeds:
        logger.info(f"Fetching feed: {feed_url}")
        feed_data = fetch_feed(feed_url)
        if feed_data:
            # TODO: Store feed data in vector database
            logger.info(f"Successfully fetched {len(feed_data['entries'])} entries from {feed_data['title']}")

if __name__ == "__main__":
    while True:
        main()
        # Sleep for an hour
        time.sleep(3600) 