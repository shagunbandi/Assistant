import logging

from langchain_core.tools import StructuredTool
from pydantic import BaseModel

from tools.gmail_live_tool import search_gmail_service
from tools.gmail_rag_tool import query_gmail_vector_store

logger = logging.getLogger(__name__)


class CombinedGmailSearchInput(BaseModel):
    query: str  # Search query for Gmail (e.g., "label:inbox")


def combined_gmail_search(query: str):
    """
    First search the Gmail RAG vector store. If no results are found,
    fallback to the live Gmail search service.
    """
    try:
        # Step 1: Query the RAG vector store
        live_results = search_gmail_service(query=query)
        if live_results:
            return {"source": "Live Gmail Search", "results": live_results}

        # Step 2: Fallback to live Gmail search if RAG has no results
        logger.info("No results in live results found. Falling back to rag search.")
        rag_results = query_gmail_vector_store(query)

        if rag_results:
            logger.info("Found results in RAG vector store.")
            return {"source": "RAG Vector Store", "results": rag_results}

    except Exception as e:
        logger.error(f"Error in combined Gmail search: {e}")
        return {"source": "Error", "results": str(e)}


# Define the tool
search_gmail_combined_tool = StructuredTool(
    name="search_gmail_combined",
    description=(
        "Search Gmail for relevant emails. It first queries the Gmail RAG vector store. "
        "If no results are found, it falls back to a live Gmail search."
    ),
    func=combined_gmail_search,
    args_schema=CombinedGmailSearchInput,
)
