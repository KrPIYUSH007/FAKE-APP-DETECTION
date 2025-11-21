from difflib import SequenceMatcher

def name_similarity(a: str, b: str) -> float:
    """
    Returns similarity between two strings in range 0.0–1.0
    """
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()
