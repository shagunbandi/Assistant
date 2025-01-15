import logging
import logging.config
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "application.log")

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": LOG_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "file": {
            "level": LOG_LEVEL,
            "class": "logging.FileHandler",
            "formatter": "default",
            "filename": LOG_FILE_PATH,
        },
    },
    "root": {
        "level": LOG_LEVEL,
        "handlers": ["console", "file"],
    },
    "loggers": {
        "assistant": {
            "level": LOG_LEVEL,
            "handlers": ["console", "file"],
            "propagate": False,
        },
    },
}


def setup_logging():
    """Set up logging using the predefined configuration."""
    logging.config.dictConfig(LOGGING_CONFIG)


# Initialize the logger and make it available for import
def get_logger(name=None):
    """Get a logger with a specific name, defaults to 'assistant'."""
    setup_logging()
    return logging.getLogger(name or "assistant")
