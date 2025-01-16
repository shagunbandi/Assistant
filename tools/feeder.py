import json
import random

from gnews import GNews


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

    # Pick a random topic
    random_topic = random.choice(topics)

    # Initialize GNews
    google_news = GNews(language="en", country="US", max_results=1)

    # Fetch news articles for the random topic
    news_articles = google_news.get_news_by_topic(random_topic)

    if news_articles:
        article = news_articles[0]  # Get the first article
        title = article["title"]
        content = article["description"]
        source = article["publisher"]["title"]

        # Create a JSON response
        response = {
            "topic": random_topic,
            "title": title,
            "content": content,
            "source": source,
        }

        return json.dumps(response)
    else:
        # Return a JSON response for no articles found
        response = {"error": f"No news articles found for the topic: {random_topic}"}
        return json.dumps(response)