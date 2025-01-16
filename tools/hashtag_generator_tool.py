import os

from dotenv import load_dotenv
from langchain_core.tools import StructuredTool
from openai import OpenAI
from pydantic import BaseModel, Field

from logging_config import get_logger

logger = get_logger(__name__)
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class HashtagToolInput(BaseModel):
    text: str = Field(None, description="Text for which hashtags needs to be generated")


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


hashtag_tool = StructuredTool(
    name="Hashtag Generator",
    description="Generates some hashtags based on the text provided",
    func=generate_hashtags,
    args_schema=HashtagToolInput,
)
