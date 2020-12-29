"""Special handler for container."""
from typing import List

from ..strategy import AwesomeVersionStrategy
from .base import CompareHandlerBase

VERSION_CONVERT = {"stable": 1, "beta": 2, "latest": 3, "dev": 4}


class ComparelHandlerContainer(CompareHandlerBase):
    @property
    def strategy(self) -> List[AwesomeVersionStrategy]:
        """Return a list of valid strategies for this handler."""
        return [AwesomeVersionStrategy.SPECIALCONTAINER]

    def handler(self) -> bool:
        """Compare handler."""
        if self.ver_a.strategy == AwesomeVersionStrategy.SPECIALCONTAINER:
            if self.ver_b.strategy != AwesomeVersionStrategy.SPECIALCONTAINER:
                return True
            return (
                VERSION_CONVERT[self.ver_a.string] > VERSION_CONVERT[self.ver_b.string]
            )
        if self.ver_b.strategy == AwesomeVersionStrategy.SPECIALCONTAINER:
            return False
