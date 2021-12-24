"""Regex utils for AwesomeVersion."""
import re
from typing import Match, Optional, Pattern

# General purpose patterns
RE_DIGIT = re.compile(r"[a-z]*(\d+)[a-z]*")
RE_MODIFIER = re.compile(r"^((?:\d+\-|\d|))(([a-z]+)\.?(\d*))$")


# Version patterns
RE_CALVER = r"(\d{2}|\d{4})\.\d{1,2}?(\.?\d{1,2}?\.?)?(\.\d)?(\d*(\w+\d+)?)"
RE_SEMVER = (
    r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?"
)
RE_PEP440 = (
    r"([1-9][0-9]*!)?(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))*((a|b|rc)"
    r"(0|[1-9][0-9]*))?(\.post(0|[1-9][0-9]*))?(\.dev(0|[1-9][0-9]*))?(\.rc(0|[1-9][0-9]*))?"
)
RE_BUILDVER = r"\d+"

RE_SPECIAL_CONTAINER = r"(latest|dev|stable|beta)"
RE_SIMPLE = r"[v|V]?((\d+)(\.\d+)+)"


def compile_regex(pattern: str) -> Pattern[str]:
    """Compile a regex."""
    return re.compile(pattern)


def get_regex_match_group(
    pattern: Pattern[str], string: Optional[str], group: int = 0
) -> Optional[str]:
    """Return the requested group in the regex."""
    match = pattern.match(string or "")
    return get_group_from_regex_match(match, group) if match else None


def generate_full_string_regex(string: str) -> Pattern[str]:
    """Generate a regex that matches the full string."""
    return compile_regex(r"^" + string + r"$")


def get_group_from_regex_match(match: Match[str], group: int = 0) -> Optional[str]:
    """Return the requested group in the regex."""
    try:
        return match.group(group)
    except IndexError:
        return None
