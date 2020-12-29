"""Special handler for dev."""
from .base import CompareHandlerBase


class ComparelHandlerDev(CompareHandlerBase):
    def handler(self) -> bool:
        """Compare handler."""
        a_last = self.ver_a.string.split(".")[-1]
        b_last = self.ver_b.string.split(".")[-1]
        if not a_last.startswith("dev") and b_last.startswith("dev"):
            self.ver_b._version = self.ver_b.string.replace(b_last, "0")
            if self.ver_a.string == self.ver_b.string:
                return True
