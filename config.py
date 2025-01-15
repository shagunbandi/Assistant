import os

current_dir = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(current_dir, "rag", "data", "emails.json")
persistent_directory = os.path.join(current_dir, "rag", "db", "chroma_db")

EMAIL_LABELS = [
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
]
MAX_RESULTS = 10
EMBEDDING_MODEL = "text-embedding-ada-002"
