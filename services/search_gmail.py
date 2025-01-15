from typing import List, Dict
import os
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
import re

# If modifying these SCOPES, delete the token.json file
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def _authenticate_gmail():
    """Authenticate and return the Gmail API service."""
    creds = None
    # Check if token.json exists for saved credentials
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If no valid credentials, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for future use
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    # Build the Gmail API service
    return build("gmail", "v1", credentials=creds)


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


def _get_label_mapping():
    """Fetch label mapping (name to ID and ID to name) from Gmail API."""
    service = _authenticate_gmail()
    results = service.users().labels().list(userId="me").execute()
    labels = results.get("labels", [])
    label_name_to_id = {label["name"]: label["id"] for label in labels}
    label_id_to_name = {label["id"]: label["name"] for label in labels}
    return label_name_to_id, label_id_to_name


def search_gmail_service(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """Search Gmail for the top relevant emails matching the query."""
    service = _authenticate_gmail()

    try:
        # Fetch label mapping
        _, label_id_to_name = _get_label_mapping()

        # Search for emails with pagination
        emails = []
        next_page_token = None

        while len(emails) < max_results:
            # Limit the number of results per API call to 500
            page_results = min(max_results - len(emails), 500)

            results = (
                service.users()
                .messages()
                .list(
                    userId="me",
                    q=query,
                    maxResults=page_results,
                    pageToken=next_page_token,
                )
                .execute()
            )
            messages = results.get("messages", [])
            next_page_token = results.get("nextPageToken")

            # Fetch details for each email
            for msg in messages:
                msg_id = msg["id"]
                msg_data = (
                    service.users()
                    .messages()
                    .get(userId="me", id=msg_id, format="full")
                    .execute()
                )
                payload = msg_data.get("payload", {})
                headers = payload.get("headers", [])
                subject = next(
                    (
                        header["value"]
                        for header in headers
                        if header["name"] == "Subject"
                    ),
                    "No Subject",
                )
                sender = next(
                    (header["value"] for header in headers if header["name"] == "From"),
                    "Unknown Sender",
                )
                timestamp = (
                    int(msg_data.get("internalDate", 0)) // 1000
                )  # Convert to seconds
                labels = msg_data.get("labelIds", [])
                # Map label IDs to names
                labels = [label_id_to_name.get(label, label) for label in labels]
                body = ""

                # Decode the email body content
                if "parts" in payload:
                    for part in payload["parts"]:
                        if part["mimeType"] == "text/plain" and "data" in part["body"]:
                            body += base64.urlsafe_b64decode(
                                part["body"]["data"]
                            ).decode("utf-8")
                elif "body" in payload and "data" in payload["body"]:
                    body += base64.urlsafe_b64decode(payload["body"]["data"]).decode(
                        "utf-8"
                    )

                emails.append(
                    {
                        "id": msg_id,
                        "subject": subject,
                        "from": sender,
                        "timestamp": timestamp,
                        "labels": labels,
                        "body": _clean_email_body(body),
                    }
                )

            if not next_page_token:
                break

        return emails

    except Exception as error:
        raise RuntimeError(f"An error occurred: {error}")
