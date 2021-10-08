""""Custom types for AwesomeVersion."""
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .awesomeversion import AwesomeVersion

Version = Union[str, float, int, object, "AwesomeVersion"]
