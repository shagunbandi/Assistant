import os
from langchain_chroma import Chroma  # Updated import for Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.tools import StructuredTool
from pydantic import BaseModel
from config import EMBEDDING_MODEL, current_dir, persistent_directory

# Define the embedding model
embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

# Load the existing vector store with the embedding function
db = Chroma(persist_directory=persistent_directory, embedding_function=embeddings)


class GmailQueryInput(BaseModel):
    query: str


def query_gmail_vector_store(query: str):
    """Query the Gmail-based vector store and retrieve relevant documents."""
    retriever = db.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"k": 3, "score_threshold": 0.5},
    )
    relevant_docs = retriever.invoke(query)

    # Format the results
    results = []
    for i, doc in enumerate(relevant_docs, 1):
        result = {
            "Document": i,
            "Content": doc.page_content,
            "Metadata": doc.metadata,
        }
        results.append(result)

    return results


# Define the tool
search_gmail_rag_tool = StructuredTool(
    name="search_gmail_rag_tool",
    description="Query the Gmail-based vector store for relevant emails based on user questions.",
    func=query_gmail_vector_store,
    args_schema=GmailQueryInput,
)
