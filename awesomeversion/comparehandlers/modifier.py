"""Special handler for modifier."""
from .base import CompareHandlerBase


class ComparelHandlerModifier(CompareHandlerBase):
    def handler(self) -> bool:
        """Compare handler."""
        if not self.ver_a.modifier and self.ver_b.modifier:
            self.ver_b._version = self.ver_b.string.replace(self.ver_b.modifier, "")
            if self.ver_a.string == self.ver_b.string:
                return True

        if self.ver_a.modifier and not self.ver_b.modifier:
            self.ver_a._version = self.ver_a.string.replace(self.ver_a.modifier, "")
