"""AwesomeVersion strategy base."""
import re
from typing import Optional, Union

from ..const import AwesomeVersionStrategy


class AwesomeVersionStrategyBase:
    """Base strategy class."""

    REGEX_MATCH: Optional[re.Pattern] = None
    STRATEGY: Union[AwesomeVersionStrategy, str] = "Custom"

    def __init__(self, version: str):
        """Initialize."""
        self.version = version

    @property
    def version_matches(self) -> Optional[bool]:
        """Do not ovveride this in subclass, use match instead."""
        if self.REGEX_MATCH is not None:
            return self.REGEX_MATCH.match(self.version)
        return self.match()

    def match(self) -> Optional[bool]:
        """Return true if the version matches this strategy."""
        raise NotImplementedError
