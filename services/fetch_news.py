import random
from typing import Dict, Optional

from gnews import GNews

from logging_config import get_logger

logger = get_logger(__name__)


def fetch_news_article(
    keyword: Optional[str] = None,
    language: str = "en",
    country: str = "IN",
) -> Optional[Dict[str, str]]:
    google_news = GNews(language=language, country=country, max_results=1)

    if keyword:
        news_articles = google_news.get_news(keyword)
        topic = keyword.upper()
    else:
        topics = [
            "WORLD",
            "SCIENCE",
            "ECONOMY",
            "ENERGY",
            "VIRTUAL REALITY",
            "ROBOTICS",
            "NUTRITION",
            "MENTAL HEALTH",
            "WILDLIFE",
            "ENVIRONMENT",
            "NEUROSCIENCE",
            "JOBS",
            "FOOD",
            "TRAVEL",
        ]
        topic = random.choice(topics)
        news_articles = google_news.get_news_by_topic(topic)

    if news_articles:
        article = news_articles[0]
        return {
            "topic": topic,
            "title": article["title"],
            "content": article["description"],
            "source": article["publisher"]["title"],
        }
    else:
        logger.warning(f"No news articles found for the topic/keyword: {topic}")
        return None
