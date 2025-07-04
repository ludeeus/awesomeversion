"""Regex utils for AwesomeVersion."""

import re
from functools import lru_cache
from typing import Pattern

# General purpose patterns - optimized
RE_IS_SINGLE_DIGIT = re.compile(r"^\d$")  # Simplified from ^\d{1}$
RE_DIGIT = re.compile(r"[a-z]*(\d+)[a-z]*")
RE_MODIFIER = re.compile(r"^((?:\d+\-|\d|))(([a-z]+)\.?(\d*))$")


# Version patterns - optimized for performance while maintaining compatibility
# CalVer: Keep original pattern to maintain exact matching behavior
RE_CALVER = r"(\d{2}|\d{4})\.\d{1,2}?(\.?\d{1,2}?\.?)?(\.\d)?(\d*(\w+\d+)?)"

# SemVer: Maintain capture groups for modifier extraction while optimizing performance
RE_SEMVER = (
    r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?"
)

# PEP440: Slightly optimized with non-capturing groups where possible
RE_PEP440 = (
    r"([1-9][0-9]*!)?(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))*"  # Main segment
    r"([-_\.]?(?:alpha|beta|c|pre|preview|a|b|rc)(0|[1-9][0-9]*))?"  # Pre-release segment  
    r"([-_\.]?(?:post|r|rev)(0|[1-9][0-9]*))?"  # Post-release segment
    r"([-_\.]?(?:d|dev)(0|[1-9][0-9]*))?"  # Development release segment
    r"(?:\+([a-z0-9]+(?:[-_\.][a-z0-9]+)*))?"  # Local version segment
)

# Simple patterns
RE_BUILDVER = r"\d+"
RE_HEXVER = r"0x[A-Fa-f0-9]+"

# Special container - use non-capturing group for better performance
RE_SPECIAL_CONTAINER = r"(?:latest|dev|stable|beta)"

# Simple version pattern
RE_SIMPLE = r"[v|V]?((\d+)(\.\d+)+)"


@lru_cache(maxsize=128)  # Increased cache size for regex compilation
def compile_regex(pattern: str) -> Pattern[str]:
    """Compile a regex with caching to avoid recompilation."""
    return re.compile(pattern)


@lru_cache(maxsize=32)  # Smaller cache for full string patterns (fewer unique patterns)
def generate_full_string_regex(string: str) -> Pattern[str]:
    """Generate a regex that matches the full string with caching."""
    return compile_regex(r"^" + string + r"$")


# Pre-compile frequently used patterns for maximum performance
_COMPILED_PATTERNS = {
    'BUILDVER_FULL': re.compile(r"^\d+$"),
    'HEXVER_FULL': re.compile(r"^0x[A-Fa-f0-9]+$"),
    'SPECIAL_CONTAINER_FULL': re.compile(r"^(?:latest|dev|stable|beta)$"),
    'IS_SINGLE_DIGIT': RE_IS_SINGLE_DIGIT,
    'DIGIT': RE_DIGIT,
    'MODIFIER': RE_MODIFIER,
}


def get_compiled_pattern(pattern_name: str) -> Pattern[str] | None:
    """Get a pre-compiled pattern for maximum performance."""
    return _COMPILED_PATTERNS.get(pattern_name)
