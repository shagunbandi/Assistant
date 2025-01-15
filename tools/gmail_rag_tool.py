from langchain_chroma import Chroma  # Updated import
from langchain_huggingface import HuggingFaceEmbeddings  # Updated import
from langchain_core.tools import StructuredTool
from pydantic import BaseModel
from config import (
    EMBEDDING_MODEL,
    persistent_directory,
    NUMBER_OF_DOCUMENTS,
    SCORE_THRESHOLD,
)

# Define the embedding model using HuggingFace
embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

# Load the existing vector store with the embedding function
db = Chroma(persist_directory=persistent_directory, embedding_function=embeddings)


class GmailQueryInput(BaseModel):
    query: str


def query_gmail_vector_store(query: str):
    """Query the Gmail-based vector store and retrieve relevant documents."""
    retriever = db.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"k": NUMBER_OF_DOCUMENTS, "score_threshold": SCORE_THRESHOLD},
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
