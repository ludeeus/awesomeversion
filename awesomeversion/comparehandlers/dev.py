"""Special handler for dev."""
from typing import Optional

from .sections import ComparelHandlerSections


class ComparelHandlerDev(ComparelHandlerSections):
    """ComparelHandlerDev class."""

    def handler(self) -> Optional[bool]:
        """Compare handler."""
        a_last = self.ver_a.string.split(".")[-1]
        b_last = self.ver_b.string.split(".")[-1]
        if not a_last.startswith("dev") and b_last.startswith("dev"):
            self.ver_b._version = self.ver_b.string.replace(f".{b_last}", "")
            if self.ver_a.string == self.ver_b.string:
                return True
            if self._compare_base_sections(self.ver_a, self.ver_b) is None:
                return True
