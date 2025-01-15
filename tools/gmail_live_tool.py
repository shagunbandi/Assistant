from pydantic import BaseModel
from langchain_core.tools import StructuredTool
from services.search_gmail import search_gmail_service
import logging

logger = logging.getLogger(__name__)


class GmailSearchInput(BaseModel):
    query: str  # Search query for Gmail (e.g., "label:inbox")


# Define the tool
search_gmail_live_tool = StructuredTool(
    name="search_gmail_live",
    description="Search Gmail for relevant emails based on a query.",
    func=search_gmail_service,
    args_schema=GmailSearchInput,
)