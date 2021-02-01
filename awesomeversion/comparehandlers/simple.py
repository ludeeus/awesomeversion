"""Special handler for simple."""
from typing import Optional

from awesomeversion.strategy import AwesomeVersionStrategy

from .sections import ComparelHandlerSections


class ComparelHandlerSimple(ComparelHandlerSections):
    """ComparelHandlerSimple class."""

    def handler(self) -> Optional[bool]:
        """Compare handler."""
        if self.ver_a.simple and self.ver_b.simple:
            if self._compare_base_sections(self.ver_a, self.ver_b) is None:
                return False

        if self.ver_a.simple and self.ver_b.strategy not in [
            AwesomeVersionStrategy.SPECIALCONTAINER
        ]:
            if self._compare_base_sections(self.ver_a, self.ver_b) is None:
                return True
