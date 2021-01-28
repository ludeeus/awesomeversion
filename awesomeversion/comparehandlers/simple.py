"""Special handler for simple."""
from .sections import ComparelHandlerSections


class ComparelHandlerSimple(ComparelHandlerSections):
    def handler(self) -> bool:
        """Compare handler."""
        if self.ver_a.simple and self.ver_b.simple:
            base = self._compare_base_sections(self.ver_a, self.ver_b)
            if base is not None:
                return base
            return self._compare_modifier_section(self.ver_a, self.ver_b)
