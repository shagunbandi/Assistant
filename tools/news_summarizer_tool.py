import json
import logging
import os
import random

from dotenv import load_dotenv
from gnews import GNews
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_core.tools import StructuredTool
from openai import OpenAI
from pydantic import BaseModel, Field, ValidationError

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
logger = logging.getLogger(__name__)


class NewsToolInput(BaseModel):
    keyword: str = Field(
        None, description="Optional keyword to search for specific news"
    )


class NewsArticle(BaseModel):
    topic: str = Field(..., description="The topic of the news article")
    title: str = Field(..., description="The title of the news article")
    content: str = Field(..., description="The content of the news article")
    source: str = Field(..., description="The source of the news article")
    summary: str = Field(..., description="A 60-word summary of the news article")
    hashtags: list[str] = Field(
        ..., description="10 trending Instagram hashtags for the news"
    )


def fetch_news_article(keyword=None):
    google_news = GNews(language="en", country="US", max_results=1)
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


class NewsSummary(BaseModel):
    summary: str
    hashtags: list[str]


# Define the output parser
parser = PydanticOutputParser(pydantic_object=NewsSummary)


def summarize_news(news_content):
    try:
        # Define the prompt template
        prompt_template = ChatPromptTemplate.from_template(
            """Summarize the following news article in 60 words or less and provide 10 trending Instagram hashtags related to the content.
            Return the result as a JSON object with two keys: 'summary' and 'hashtags'.

            News article:
            {news_content}

            Response format:
            {{
                "summary": "Your 60-word summary here",
                "hashtags": ["#hashtag1", "#hashtag2", ..., "#hashtag10"]
            }}
            """
        )

        prompt = prompt_template.format_prompt(news_content=news_content)

        # Get GPT response
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes news articles and generates relevant hashtags.",
                },
                {"role": "user", "content": prompt.to_string()},
            ],
            temperature=0.7,
        )

        # Parse response with LangChain
        parsed_response = parser.parse(response.choices[0].message.content.strip())
        return parsed_response.dict()
    except ValidationError as ve:
        logger.error(f"Validation error in response parsing: {ve}")
    except Exception as e:
        logger.error(f"Error in summarizing news: {str(e)}")
        return None


def news_summarizer_tool(keyword: str = None) -> NewsArticle:
    article = fetch_news_article(keyword)
    if not article:
        raise ValueError("Failed to fetch a news article")

    summary_result = summarize_news(article["content"])
    if not summary_result:
        raise ValueError("Failed to summarize the news article")

    return NewsArticle(
        topic=article["topic"],
        title=article["title"],
        content=article["content"],
        source=article["source"],
        summary=summary_result["summary"],
        hashtags=summary_result["hashtags"],
    )


news_tool = StructuredTool(
    name="News Summarizer",
    description="Fetches a news article (random or based on keyword), summarizes it, and generates related hashtags",
    func=news_summarizer_tool,
    args_schema=NewsToolInput,
)

if __name__ == "__main__":
    try:
        # Example usage without keyword
        result = news_tool.run({})
        print(json.dumps(result.dict(), indent=2))

        # Example usage with keyword
        result_with_keyword = news_tool.run({"keyword": "artificial intelligence"})
        print(json.dumps(result_with_keyword.dict(), indent=2))
    except Exception as e:
        logger.error(f"Error running news tool: {str(e)}")
