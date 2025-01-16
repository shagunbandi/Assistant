import json
import random
import os
from openai import OpenAI
from dotenv import load_dotenv
from gnews import GNews

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def fetch_random_news_article():
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

    random_topic = random.choice(topics)
    google_news = GNews(language="en", country="US", max_results=1)
    news_articles = google_news.get_news_by_topic(random_topic)

    if news_articles:
        article = news_articles[0]
        return {
            "topic": random_topic,
            "title": article["title"],
            "content": article["description"],
            "source": article["publisher"]["title"],
        }
    else:
        return {"error": f"No news articles found for the topic: {random_topic}"}


def summarize_news(news_content):
    prompt = f"Summarize this news article in 60 words:\n\n{news_content}"
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=60,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()


def generate_hashtags(summary):
    prompt = (
        f"Generate 10 trending Instagram hashtags for this news summary:\n\n{summary}"
    )
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=50,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    article = fetch_random_news_article()

    if "error" in article:
        print(article)
    else:
        print(f"Title: {article['title']}")
        print(f"Content: {article['content']}")

        summary = summarize_news(article["content"])
        print("\nSummarized News (60 words):", summary)

        hashtags = generate_hashtags(summary)
        print("\nInstagram Hashtags:", hashtags)
