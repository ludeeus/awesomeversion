"""Special handler for simple."""
from .sections import ComparelHandlerSections


class ComparelHandlerSimple(ComparelHandlerSections):
    """ComparelHandlerSimple class."""

    def handler(self) -> bool:
        """Compare handler."""
        if self.ver_a.simple and self.ver_b.simple:
            return self._compare_base_sections(self.ver_a, self.ver_b)
