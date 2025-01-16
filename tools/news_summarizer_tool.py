import os

from dotenv import load_dotenv
from langchain_core.tools import StructuredTool
from openai import OpenAI
from pydantic import BaseModel, Field

from logging_config import get_logger
from services.fetch_news import fetch_news_article

logger = get_logger(__name__)
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class NewsToolInput(BaseModel):
    keyword: str = Field(
        None, description="Optional keyword to search for specific news"
    )
    language: str = Field(
        "en", description="Language of the news articles (default is English)"
    )
    country: str = Field(
        "US", description="Country code for news articles (default is US)"
    )


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


def news_summarizer(
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


news_tool = StructuredTool(
    name="News Summarizer",
    description="Fetches a news article (random or based on keyword), summarizes it",
    func=news_summarizer,
    args_schema=NewsToolInput,
)
