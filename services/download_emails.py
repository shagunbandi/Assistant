import os
import json
from services.search_gmail import search_gmail_service
from bs4 import BeautifulSoup
import re
from logging_config import get_logger

logger = get_logger(__name__)


def _clean_email_body(body: str) -> str:
    """Clean the email body by removing HTML, CSS, and non-human-readable content."""
    soup = BeautifulSoup(body, "html.parser")
    clean_text = soup.get_text(separator="\n").strip()
    # Replace multiple newlines (\n) with a single newline
    clean_text = re.sub(r"\n+", "\n", clean_text)

    # Replace multiple newlines (\n) with a single newline
    clean_text = re.sub(r"\r+", "\r", clean_text)

    # Replace multiple spaces with a single space
    clean_text = re.sub(r"\s+", " ", clean_text)

    return clean_text.strip()


def fetch_emails_to_json(
    labels=[
        "label:inbox",
        "label:starred",
        "label:important",
    ],
    query=None,
    max_results=10,
    download_json_file_path=None,
):
    """Fetch emails using the Gmail tool for multiple labels or query and save them to a JSON file."""
    if not os.path.exists(download_json_file_path):
        all_emails = []

        if query:
            logger.info(f"Fetching emails with query: {query}")
            emails = search_gmail_service(query=query, max_results=max_results)

            # Clean email bodies
            for email in emails:
                email["body"] = _clean_email_body(email.get("body", ""))

            all_emails.extend(emails)
        else:
            combined_query = " OR ".join(labels)
            logger.info(f"Fetching emails with combined query: {combined_query}")
            emails = search_gmail_service(query=combined_query, max_results=max_results)

            # Clean email bodies and resolve labels
            for email in emails:
                email["body"] = _clean_email_body(email.get("body", ""))

            all_emails.extend(emails)

        # Save all cleaned emails to JSON
        logger.info(f"Saving {len(all_emails)} emails to {download_json_file_path}...")
        with open(download_json_file_path, "w", encoding="utf-8") as json_file:
            json.dump(all_emails, json_file, ensure_ascii=False, indent=4)
        logger.info(
            f"Saved {len(all_emails)} cleaned emails to {download_json_file_path}"
        )
    else:
        logger.info("JSON file already exists. Skipping email fetch.")
