import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain.schema.runnable import RunnableLambda
from openai import OpenAI

# Load environment variables from .env
load_dotenv()

# Create a ChatOpenAI model
model = ChatOpenAI(model="gpt-4o")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define prompt templates (no need for separate Runnable chains)
prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert at creating prompts in less than 60 words for a given summary",
        ),
        ("human", "The summary is: {summary}"),
    ]
)

# Use RunnableLambda for image generation
generate_image_lambda = RunnableLambda(
    lambda x: client.images.generate(prompt=x, n=1, size="1024x1024").data[0].url
)

chain = prompt_template | model | StrOutputParser() | generate_image_lambda

# Example summarized news
summarized_news = "On Day 4 of the Mahakumbh Mela 2025, held at Sangam, millions of devotees defied the biting cold to partake in the sacred ritual of a holy dip. The event has already seen participation from over 6 crore individuals. The Mahakumbh Mela continues to draw massive crowds, highlighting its significant cultural and spiritual importance."

result = chain.invoke({"summary": summarized_news})
