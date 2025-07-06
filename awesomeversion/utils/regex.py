"""Regex utils for AwesomeVersion."""

from __future__ import annotations

from functools import lru_cache
import re
from typing import Pattern

RE_IS_SINGLE_DIGIT = re.compile(r"^\d$")
RE_DIGIT = re.compile(r"[a-z]*(\d+)[a-z]*")
RE_MODIFIER = re.compile(r"^((?:\d+\-|\d|))(([a-z]+)\.?(\d*))$")
RE_COMPOUND_MODIFIER = re.compile(r"^([a-z]+)(\d*)-.*$")
RE_MODIFIER_COMPOUND_PART = re.compile(r"^([a-z]+)(\d*)$")


RE_CALVER = r"(\d{2}|\d{4})\.\d{1,2}?(\.?\d{1,2}?\.?)?(\.\d)?(\d*(\w+\d+)?)"

RE_SEMVER = (
    r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?"
)


RE_PEP440 = (
    r"([1-9][0-9]*!)?(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))*"
    r"([-_\.]?(?:alpha|beta|c|pre|preview|a|b|rc)(0|[1-9][0-9]*))?"
    r"([-_\.]?(?:post|r|rev)(0|[1-9][0-9]*))?"
    r"([-_\.]?(?:d|dev)(0|[1-9][0-9]*))?"
    r"(?:\+([a-z0-9]+(?:[-_\.][a-z0-9]+)*))?"
)

RE_BUILDVER = r"\d+"
RE_HEXVER = r"0x[A-Fa-f0-9]+"

RE_SPECIAL_CONTAINER = r"(?:latest|dev|stable|beta)"

RE_SIMPLE = r"[vV]?((\d+)(\.\d+)+)"


@lru_cache(maxsize=128)
def compile_regex(pattern: str) -> Pattern[str]:
    """Compile a regex with caching to avoid recompilation."""
    return re.compile(pattern)


@lru_cache(maxsize=32)
def generate_full_string_regex(string: str) -> Pattern[str]:
    """Generate a regex that matches the full string with caching."""
    return compile_regex(r"^" + string + r"$")


@lru_cache(maxsize=64)
def match_compound_modifier(modifier: str) -> re.Match[str] | None:
    """Match compound modifiers with caching for performance."""
    return RE_COMPOUND_MODIFIER.match(modifier)


@lru_cache(maxsize=128)
def match_modifier_compound_part(part: str) -> re.Match[str] | None:
    """Match modifier parts with caching for performance."""
    return RE_MODIFIER_COMPOUND_PART.match(part)


@lru_cache(maxsize=256)
def extract_digits(text: str) -> list[str]:
    """Extract all digits from text with caching for performance."""
    return re.findall(r"(\d+)", text)


_COMPILED_PATTERNS = {
    "BUILDVER_FULL": re.compile(r"^\d+$"),
    "HEXVER_FULL": re.compile(r"^0x[A-Fa-f0-9]+$"),
    "SPECIAL_CONTAINER_FULL": re.compile(r"^(?:latest|dev|stable|beta)$"),
    "IS_SINGLE_DIGIT": RE_IS_SINGLE_DIGIT,
    "DIGIT": RE_DIGIT,
    "MODIFIER": RE_MODIFIER,
}


def get_compiled_pattern(pattern_name: str) -> Pattern[str] | None:
    """Get a pre-compiled pattern for maximum performance."""
    return _COMPILED_PATTERNS.get(pattern_name)
