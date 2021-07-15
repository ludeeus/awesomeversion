"""AwesomeVersion strategy base."""
from enum import Enum
from typing import Optional
import re


class AwesomeVersionStrategyBase:
    """Base strategy class."""

    REGEX_MATCH: Optional[re.Pattern] = None
    STRATEGY: Optional[str] = None

    def __init__(self, version: str):
        """Initialize."""
        self.version = version

    @property
    def version_matches(self) -> bool:
        """Do not ovveride this in subclass, use match instead."""
        if self.REGEX_MATCH is not None:
            return self.REGEX_MATCH.match(self.version)
        return self.match()

    def match(self) -> bool:
        """Return true if the version matches this strategy."""
        raise NotImplementedError
