"""Special handler for simple."""
from typing import Optional

from ..const import AwesomeVersionStrategy
from .sections import AwesomeVersionCompareHandlerSections


class AwesomeVersionCompareHandlerSimple(AwesomeVersionCompareHandlerSections):
    """AwesomeVersionCompareHandlerSimple class."""

    def handler(self) -> Optional[bool]:
        """Compare handler."""
        if self.version_a.simple and self.version_b.simple:
            if self._compare_base_sections(self.version_a, self.version_b) is None:
                return False

        if self.version_a.simple and self.version_b.strategy not in [
            AwesomeVersionStrategy.SPECIALCONTAINER
        ]:
            if self._compare_base_sections(self.version_a, self.version_b) is None:
                return True
