"""AwesomeVersion strategy base."""
from __future__ import annotations
import re
from ..const import AwesomeVersionStrategy


class AwesomeVersionStrategyBase:
    """Base strategy class."""

    REGEX_MATCH: re.Pattern | None = None
    STRATEGY: AwesomeVersionStrategy | str | None = "Custom"

    def __init__(self, version: str):
        """Initialize."""
        self.version = version

    @property
    def version_matches(self) -> bool | None:
        """Do not ovveride this in subclass, use match instead."""
        if self.REGEX_MATCH is not None:
            return self.REGEX_MATCH.match(self.version)
        return self.match()

    def match(self) -> bool | None:
        """Return true if the version matches this strategy."""
        raise NotImplementedError
