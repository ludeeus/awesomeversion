""""Custom types for AwesomeVersion."""
from typing import TYPE_CHECKING, List, Optional, Tuple, Union

from .strategy import AwesomeVersionStrategy

if TYPE_CHECKING:
    from .awesomeversion import AwesomeVersion

VersionType = Union[str, float, int, object, "AwesomeVersion"]
EnsureStrategyIterableType = Union[
    List[AwesomeVersionStrategy],
    Tuple[AwesomeVersionStrategy, ...],
]
EnsureStrategyType = Optional[
    Union[
        AwesomeVersionStrategy,
        EnsureStrategyIterableType,
    ]
]
