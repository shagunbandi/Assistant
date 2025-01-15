from pydantic import BaseModel
from langchain_core.tools import StructuredTool
from services.search_gmail_service import search_gmail_service


class GmailSearchInput(BaseModel):
    query: str  # Search query for Gmail (e.g., "label:inbox")
    max_results: int = 10  # Maximum number of results to retrieve


# Define the tool
search_gmail_live_tool = StructuredTool(
    name="search_gmail_live",
    description="Search Gmail for relevant emails based on a query.",
    func=search_gmail_service,
    args_schema=GmailSearchInput,
)

# Example usage
if __name__ == "__main__":
    input_data = {"query": "label:inbox", "max_results": 2}
    try:
        results = search_gmail_live_tool.run(input_data)
        for i, email in enumerate(results, 1):
            print(f"Email {i}:")
            print(f"Subject: {email['subject']}")
            print(f"From: {email['from']}")
            print(f"Timestamp: {email['timestamp']}")
            print(f"Labels: {', '.join(email['labels'])}")
            print(f"Body: {email['body']}\n")
    except Exception as e:
        print(f"Error: {e}")
