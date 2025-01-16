from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from services.fetch_news import fetch_news_article


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


news_tool = StructuredTool(
    name="News Summarizer",
    description="Fetches a news article (random or based on keyword), summarizes it",
    func=fetch_news_article,
    args_schema=NewsToolInput,
)
