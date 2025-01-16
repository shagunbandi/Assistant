import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Initialize the OpenAI client with the API key from environment variables
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def create_prompt_using_chatgpt(summary):
    """
    Generate a detailed image prompt using ChatGPT based on the summarized news.
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": f"Generate a detailed image prompt based on the following summary: {summary}. Use no more than 60 words",
            }
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content


def generate_image(prompt):
    """
    Generate an image based on a given text prompt using DALL·E 3.
    """
    response = client.images.generate(
        prompt=prompt, n=1, size="1024x1024"  # Using a larger size for better quality
    )

    image_url = response.data[0].url
    return image_url


if __name__ == "__main__":
    # Example summarized news
    summarized_news = "A recent article from SitePoint discusses the best programming languages for AI development, highlighting Python, R, and Julia. Python is recognized for its extensive libraries and community support, making it a favored choice for AI projects. R is valued for its capabilities in statistical analysis, while Julia is noted for its high-performance capabilities. The article also explores other languages suitable for AI, emphasizing their unique strengths and applications."

    # Create a prompt using ChatGPT based on the summarized news
    prompt = create_prompt_using_chatgpt(summarized_news)

    print(prompt)

    # Generate an image based on the created prompt
    print("Generating image for summarized news...")

    image_url = generate_image(prompt)

    print("Generated Image URL:", image_url)
