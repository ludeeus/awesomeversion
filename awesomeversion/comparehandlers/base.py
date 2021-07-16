"""Base compare handler."""
from typing import TYPE_CHECKING, Optional, Union

from ..const import AwesomeVersionStrategy

if TYPE_CHECKING:
    from ..awesomeversion import AwesomeVersion


class AwesomeVersionCompareHandler:
    """CompareHandlerBase class."""

    STRATEGIES: Union[list[AwesomeVersionStrategy, str]] = []

    def __init__(
        self, version_a: "AwesomeVersion", version_b: "AwesomeVersion"
    ) -> None:
        """Initialize the special handler base_class."""
        self.version_a = version_a
        self.version_b = version_b

    @property
    def strategy(self) -> Union[list[AwesomeVersionStrategy, str]]:
        """Return a list of valid strategies for this handler."""
        return self.STRATEGIES

    def handler(self) -> Optional[bool]:
        """Compare handler."""
        raise NotImplementedError
