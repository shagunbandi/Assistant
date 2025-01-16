import os

from dotenv import load_dotenv
from openai import OpenAI

from logging_config import get_logger

logger = get_logger(__name__)
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_hashtags(text):
    """
    Generate 10 trending Instagram hashtags based on the text provided.
    """
    prompt = f"Generate 10 trending Instagram hashtags for the text provided. Return them space-separated without commas or numbering. Eg. #hashtag1 #hashtag2 ... #hashtag10:\n\n{text}"

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    hashtags = response.choices[0].message.content.split()
    return hashtags
