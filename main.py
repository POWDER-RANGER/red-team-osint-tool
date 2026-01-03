#!/usr/bin/env python3
"""
Red Team OSINT Tool

This tool provides a basic framework for performing open-source intelligence (OSINT)
and dark-web monitoring tasks using Python. It fetches a target URL and parses
the title of the page. Optional Tor support is included for anonymized requests,
but a local Tor service (e.g., via the Tor Browser Bundle or system service) must
already be running on the host machine.

Note: This code is provided for legitimate security research and reconnaissance
purposes only. Do not use it to access systems or data without permission.
"""
import argparse
import requests
from bs4 import BeautifulSoup


def fetch_url(url: str, use_tor: bool = False) -> str:
    """Fetch the contents of a URL.

    If use_tor is True, the request will be routed through a local Tor
    SOCKS proxy. Ensure that Tor is running on 127.0.0.1:9050 before
    enabling this option.

    Args:
        url: The URL to fetch.
        use_tor: Whether to route the request through Tor.

    Returns:
        The HTML content of the page.
    """
    session = requests.Session()
    if use_tor:
        session.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }
    response = session.get(url, timeout=10)
    response.raise_for_status()
    return response.text


def parse_html(html: str) -> str:
    """Extract the title from HTML.

    Args:
        html: HTML content as a string.

    Returns:
        The text of the <title> tag, or a placeholder if not found.
    """
    soup = BeautifulSoup(html, 'html.parser')
    return soup.title.text.strip() if soup.title else 'No title found'


def main() -> None:
    """Command-line entry point."""
    parser = argparse.ArgumentParser(description='Red Team OSINT Tool')
    parser.add_argument('url', help='URL to fetch and parse')
    parser.add_argument(
        '--tor', action='store_true',
        help='Route requests through Tor (requires local Tor service running)'
    )
    args = parser.parse_args()

    try:
        html = fetch_url(args.url, use_tor=args.tor)
        title = parse_html(html)
        print(f'Title: {title}')
    except Exception as exc:
        print(f'Error fetching or parsing URL: {exc}')


if __name__ == '__main__':
    main()
