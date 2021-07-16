"""Special handler for simple."""
from __future__ import annotations

from ..const import AwesomeVersionStrategy
from .sections import ComparelHandlerSections


class ComparelHandlerSimple(ComparelHandlerSections):
    """ComparelHandlerSimple class."""

    def handler(self) -> bool | None:
        """Compare handler."""
        if self.version_a.simple and self.version_b.simple:
            if self._compare_base_sections(self.version_a, self.version_b) is None:
                return False

        if self.version_a.simple and self.version_b.strategy not in [
            AwesomeVersionStrategy.SPECIALCONTAINER
        ]:
            if self._compare_base_sections(self.version_a, self.version_b) is None:
                return True
