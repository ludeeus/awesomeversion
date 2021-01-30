"""Base compare handler."""
from typing import TYPE_CHECKING, List, Optional

from ..strategy import AwesomeVersionStrategy

if TYPE_CHECKING:
    from ..awesomeversion import AwesomeVersion


class CompareHandlerBase:
    """CompareHandlerBase class."""

    def __init__(self, ver_a: "AwesomeVersion", ver_b: "AwesomeVersion") -> None:
        """Initialize the special handler base_class."""
        self.ver_a = ver_a
        self.ver_b = ver_b

    @property
    def strategy(self) -> List[AwesomeVersionStrategy]:
        """Return a list of valid strategies for this handler."""
        return []

    def handler(self) -> Optional[bool]:
        """Compare handler."""
