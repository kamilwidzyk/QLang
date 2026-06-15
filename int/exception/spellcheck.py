import difflib

def get_spellcheck_suggestion(word: str, possibilities: list[str]) -> str | None:
    """
    Returns the closest match to 'word' from 'possibilities' using difflib
    """
    matches = difflib.get_close_matches(word, possibilities, n=1, cutoff=0.6)
    if matches:
        return matches[0]
    return None
