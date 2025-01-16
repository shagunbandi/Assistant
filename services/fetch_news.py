import os
import random
from typing import Dict, Optional

from dotenv import load_dotenv
from gnews import GNews
from openai import OpenAI
from pydantic import BaseModel, Field

from logging_config import get_logger
from services.fetch_news import fetch_news_article

logger = get_logger(__name__)
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class NewsArticle(BaseModel):
    topic: str = Field(..., description="The topic of the news article")
    title: str = Field(..., description="The title of the news article")
    content: str = Field(..., description="The content of the news article")
    source: str = Field(..., description="The source of the news article")
    summary: str = Field(..., description="A 60-word summary of the news article")


def _summarize_news(news_content):
    """
    Summarize the news content into 60 words using OpenAI.
    """
    prompt = f"Summarize this news article in 60 words:\n\n{news_content}"
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    summary = response.choices[0].message.content.strip()
    return summary


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


def fetch_summarised_news(
    keyword: str = None,
    language: str = "en",
    country: str = "US",
) -> NewsArticle:

    article = fetch_news_article(keyword, language, country)

    if not article:
        raise ValueError("Failed to fetch a news article")

    summary_result = _summarize_news(article["content"])

    if not summary_result:
        raise ValueError("Failed to summarize the news article")

    return NewsArticle(
        topic=article["topic"],
        title=article["title"],
        content=article["content"],
        source=article["source"],
        summary=summary_result,
    )
