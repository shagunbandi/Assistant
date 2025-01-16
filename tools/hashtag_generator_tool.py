from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from services.hashtag_generator import generate_hashtags


class HashtagToolInput(BaseModel):
    text: str = Field(None, description="Text for which hashtags needs to be generated")


hashtag_tool = StructuredTool(
    name="Hashtag Generator",
    description="Generates some hashtags based on the text provided",
    func=generate_hashtags,
    args_schema=HashtagToolInput,
)
