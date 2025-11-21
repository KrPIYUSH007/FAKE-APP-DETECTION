# src/similarity.py
# String similarity helper (FINAL VERSION)

from difflib import SequenceMatcher


def similarity(a: str, b: str) -> float:
    """
    Returns similarity percentage between two strings (0–100).
    Uses SequenceMatcher for token-level fuzzy matching.
    """

    if not a or not b:
        return 0.0

    ratio = SequenceMatcher(None, a.lower().strip(), b.lower().strip()).ratio()
    return ratio * 100  # convert 0–1 → 0–100
