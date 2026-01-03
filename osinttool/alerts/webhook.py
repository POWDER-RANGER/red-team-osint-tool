from __future__ import annotations
from typing import Dict, Any
import requests


def send_webhook(url: str, payload: Dict[str, Any], timeout: int = 10) -> None:
    """Send a JSON payload to a webhook URL.

    Args:
        url: The webhook endpoint URL.
        payload: A dictionary to serialize as JSON in the POST request.
        timeout: Timeout in seconds for the HTTP request.

    Raises:
        requests.HTTPError: If the response status code is not successful.
    """
    response = requests.post(url, json=payload, timeout=timeout)
    response.raise_for_status()
