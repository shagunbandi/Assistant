import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from openai import OpenAI

load_dotenv()
model = ChatOpenAI(model="gpt-4o")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_image_from_summary(summarized_news: str):
    response = client.images.generate(
        prompt=f"Generate an image that summarises the article into image: ARTICLE \n\n {summarized_news}.",
        n=3,
        size="512x512",
    )

    image_urls = [item.url for item in response.data]

    return image_urls
