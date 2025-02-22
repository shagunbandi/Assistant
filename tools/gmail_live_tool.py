from langchain_core.tools import StructuredTool
from pydantic import BaseModel

from logging_config import get_logger
from services.gmail_search import search_gmail_service

logger = get_logger(__name__)


class GmailSearchInput(BaseModel):
    query: str  # Search query for Gmail (e.g., "label:inbox")


# Define the tool
search_gmail_live_tool = StructuredTool(
    name="search_gmail_live",
    description="Search Gmail for relevant emails based on a query.",
    func=search_gmail_service,
    args_schema=GmailSearchInput,
)
