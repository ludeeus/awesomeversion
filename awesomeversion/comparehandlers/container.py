"""Special handler for container."""
from __future__ import annotations

from ..const import AwesomeVersionStrategy
from .base import AwesomeVersionCompareHandler

CONTAINER_VERSION_MAP = {"stable": 1, "beta": 2, "latest": 3, "dev": 4}


class AwesomeVersionCompareHandlerContainer(AwesomeVersionCompareHandler):
    """AwesomeVersionCompareHandlerContainer class."""

    def handler(self) -> bool | None:
        """Compare handler."""
        if self.version_a.strategy == AwesomeVersionStrategy.SPECIALCONTAINER:
            if self.version_b.strategy != AwesomeVersionStrategy.SPECIALCONTAINER:
                return True
            return (
                CONTAINER_VERSION_MAP[self.version_a.string]
                > CONTAINER_VERSION_MAP[self.version_b.string]
            )
        if self.version_b.strategy == AwesomeVersionStrategy.SPECIALCONTAINER:
            return False
