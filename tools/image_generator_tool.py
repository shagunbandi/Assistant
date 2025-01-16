import openai

# Set up OpenAI API key
openai.api_key = "your_openai_api_key"


def generate_image(prompt):
    """
    Generate an image based on a given text prompt using DALL·E.
    """
    response = openai.Image.create(prompt=prompt, n=1, size="512x512")

    image_url = response["data"][0]["url"]
    return image_url


if __name__ == "__main__":
    # Example summarized news
    summarized_news = "A major breakthrough in renewable energy has been achieved, with scientists developing a new solar panel technology that is 50% more efficient."

    # Generate an image based on the summarized news
    print("Generating image for summarized news...")

    image_url = generate_image(summarized_news)

    print("Generated Image URL:", image_url)
