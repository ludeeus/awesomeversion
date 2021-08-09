""""AwesomeVersion utilities."""
from re import Pattern
from typing import Optional


def get_regex_match_group(
    pattern: Pattern[str], string: str, group: int
) -> Optional[str]:
    """Return the requested group in the regex."""
    match = pattern.match(string)
    if match:
        try:
            return match.group(group)
        except IndexError:
            return None
    return None
