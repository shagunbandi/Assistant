import os

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import JSONLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

from config import EMBEDDING_MODEL
from logging_config import get_logger

logger = get_logger(__name__)


def initialize_vector_store(json_file_path, persistent_directory):
    """Create a vector store if it does not already exist."""
    if not os.path.exists(persistent_directory):
        logger.info("Persistent directory does not exist. Initializing vector store...")

        # Define the jq schema to parse JSON
        jq_schema = ".[] | {page_content: .body, metadata: {subject: .subject, from: .from, timestamp: .timestamp, labels: .labels}}"

        # Load the JSON file using JSONLoader with `text_content=False`
        loader = JSONLoader(
            file_path=json_file_path, jq_schema=jq_schema, text_content=False
        )
        documents = loader.load()

        # Ensure all `page_content` fields are strings
        for doc in documents:
            if not isinstance(doc.page_content, str):
                doc.page_content = str(doc.page_content)

        # Split the document into chunks based on 1000 tokens or smaller
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=100
        )
        docs = text_splitter.split_documents(documents)

        # Display information about the split documents
        logger.info("\n--- Document Chunks Information ---")
        logger.info(f"Number of document chunks: {len(docs)}")
        logger.info(f"Sample chunk:\n{docs[0].page_content}\n")

        # Create embeddings using OpenAI
        logger.info("\n--- Creating embeddings ---")
        embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
        logger.info("\n--- Finished creating embeddings ---")

        # Create the vector store and persist it automatically
        logger.info("\n--- Creating vector store ---")
        db = Chroma.from_documents(
            docs, embeddings, persist_directory=persistent_directory
        )
        logger.info(
            f"\n--- Finished creating vector store at {persistent_directory} ---"
        )

    else:
        logger.info("Vector store already exists. No need to initialize.")
