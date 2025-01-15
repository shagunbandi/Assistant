from langchain_core.tools import Tool
from wikipedia import summary


def search_wikipedia(query):
    """Searches Wikipedia and returns the summary of the first result."""
    try:
        return summary(query, sentences=2)
    except:
        return "I couldn't find any information on that."


wikipedia_tool = Tool(
    name="Wikipedia",
    func=search_wikipedia,
    description="Useful for when you need to know information about a topic.",
)
