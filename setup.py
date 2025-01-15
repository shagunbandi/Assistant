import os
from services.gmail_vector_store import initialize_vector_store
from services.download_emails import fetch_emails_to_json
from config import EMAIL_LABELS, MAX_RESULTS, json_file_path, persistent_directory


if __name__ == "__main__":
    fetch_emails_to_json(
        labels=EMAIL_LABELS,
        max_results=MAX_RESULTS,
        download_json_file_path=json_file_path,
    )
    initialize_vector_store(json_file_path, persistent_directory)
