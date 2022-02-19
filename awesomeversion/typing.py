""""Custom types for AwesomeVersion."""
from typing import TYPE_CHECKING, Union

from .strategy import AwesomeVersionStrategy

if TYPE_CHECKING:
    from .awesomeversion import AwesomeVersion

VersionType = Union[str, float, int, object, "AwesomeVersion"]
EnsureStrategyIterableType = Union[
    list[AwesomeVersionStrategy], tuple[AwesomeVersionStrategy, ...]
]


EnsureStrategyType = Union[AwesomeVersionStrategy, EnsureStrategyIterableType, None]
