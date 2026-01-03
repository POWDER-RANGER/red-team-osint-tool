import logging
from rich.logging import RichHandler


def setup_logging(level: str = "INFO") -> None:
    """Configure rich-based logging for the OSINT tool."""
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)]
    )
