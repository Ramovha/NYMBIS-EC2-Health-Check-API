"""Logging utility module."""
import os
from datetime import datetime


LOG_FILE = "logs/api.log"


def ensure_log_directory():
    """Ensure the logs directory exists."""
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)


def log_request(method, path, api_key, status_code, result):
    """Log an API request with timestamp and details.

    Args:
        method (str): HTTP method (GET, POST, etc.)
        path (str): Request path
        api_key (str): API key used (will be truncated in log)
        status_code (int): HTTP status code
        result (str): Result or error message
    """
    ensure_log_directory()

    # Truncate API key to first 10 characters for security
    api_key_display = api_key[:10] if api_key else "N/A"
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = (
        f"{timestamp} | {method} {path} | Key: {api_key_display} | "
        f"Status: {status_code} | Result: {result}\n"
    )

    with open(LOG_FILE, "a") as f:
        f.write(log_entry)
