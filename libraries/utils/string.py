import re


def is_regex_in(string: str, pattern: str) -> bool:
    """Checks if the regex pattern is in the string.

    Args:
        string: The string to check.
        pattern: The regex pattern to check.

    Returns:
        True if the regex pattern is in the string, False otherwise.
    """
    return bool(re.compile(pattern).search(string))
