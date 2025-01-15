import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import JSONLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings  # Updated import
from services.download_emails import fetch_emails_to_json

current_dir = os.path.dirname(os.path.abspath(__file__))
persistent_directory = os.path.join(current_dir, "db", "chroma_db")
json_file_path = os.path.join(current_dir, "data", "emails.json")


def initialize_vector_store():
    """Create a vector store if it does not already exist."""
    if not os.path.exists(persistent_directory):
        print("Persistent directory does not exist. Initializing vector store...")

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

        # Split the document into chunks based on per email of 1000 tokens or smaller
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=100
        )
        docs = text_splitter.split_documents(documents)

        # Display information about the split documents
        print("\n--- Document Chunks Information ---")
        print(f"Number of document chunks: {len(docs)}")
        print(f"Sample chunk:\n{docs[0].page_content}\n")

        # Create embeddings
        print("\n--- Creating embeddings ---")
        embeddings = OpenAIEmbeddings(
            model="text-embedding-ada-002"
        )  # Updated to use langchain_community
        print("\n--- Finished creating embeddings ---")

        # Create the vector store and persist it automatically
        print("\n--- Creating vector store ---")
        db = Chroma.from_documents(
            docs, embeddings, persist_directory=persistent_directory
        )
        db.persist()
        print(f"\n--- Finished creating vector store at {persistent_directory} ---")

    else:
        print("Vector store already exists. No need to initialize.")


if __name__ == "__main__":
    fetch_emails_to_json(
        labels=[
            "label:inbox",
            "label:starred",
            "label:important",
            "label:fareharbor",
            "label:geeky-navigator ",
            "label:home",
            "label:investments",
            "label:kgp",
            "label:orders",
            "label:payments-and-invoices",
            "label:to-read",
            "label:todo",
            "label:trains,-flights-and-hotels",
            "label:us-visa",
            "label:waiting",
        ],
        max_results=700,
        download_json_file_path=json_file_path,
    )
    initialize_vector_store()
