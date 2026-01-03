import difflib
from typing import Dict, Any


def compute_diff(old_text: str, new_text: str, context_lines: int = 3) -> Dict[str, Any]:
    """Compute a unified diff between old and new text and classify changes.

    Returns a dictionary with the diff text (capped to 20000 characters), the
    number of additions, deletions, and a change ratio based on the length of
    the original text.

    Args:
        old_text: The previous version of the text.
        new_text: The new version of the text.
        context_lines: Number of context lines to include in the unified diff.

    Returns:
        A dictionary containing the diff text and change statistics.
    """
    diff_lines = list(difflib.unified_diff(
        old_text.splitlines(keepends=True),
        new_text.splitlines(keepends=True),
        lineterm="",
        n=context_lines,
    ))
    additions = sum(1 for line in diff_lines if line.startswith("+") and not line.startswith("+++"))
    deletions = sum(1 for line in diff_lines if line.startswith("-") and not line.startswith("---"))
    denom = max(len(old_text.splitlines()), 1)
    return {
        "diff_text": "".join(diff_lines)[:20000],
        "additions": additions,
        "deletions": deletions,
        "change_ratio": (additions + deletions) / denom,
    }
