"""Special handler for container."""
from typing import Optional

from ..strategy import AwesomeVersionStrategy
from .base import CompareHandlerBase

CONTAINER_VERSION_MAP = {"stable": 1, "beta": 2, "latest": 3, "dev": 4}


class ComparelHandlerContainer(CompareHandlerBase):
    """ComparelHandlerContainer class."""

    def handler(self) -> Optional[bool]:
        """Compare handler."""
        if self.ver_a.strategy == AwesomeVersionStrategy.SPECIALCONTAINER:
            if self.ver_b.strategy != AwesomeVersionStrategy.SPECIALCONTAINER:
                return True
            return (
                CONTAINER_VERSION_MAP[self.ver_a.string]
                > CONTAINER_VERSION_MAP[self.ver_b.string]
            )
        if self.ver_b.strategy == AwesomeVersionStrategy.SPECIALCONTAINER:
            return False
