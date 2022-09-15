""""Custom types for AwesomeVersion."""
from __future__ import annotations

from typing import TYPE_CHECKING, List, Tuple, TypedDict, Union

from .strategy import AwesomeVersionStrategy

if TYPE_CHECKING:
    from .awesomeversion import AwesomeVersion

VersionType = Union[str, float, int, object, "AwesomeVersion"]
EnsureStrategyIterableType = Union[
    List[AwesomeVersionStrategy], Tuple[AwesomeVersionStrategy, ...]
]


EnsureStrategyType = Union[AwesomeVersionStrategy, EnsureStrategyIterableType, None]


class AwesomeVersionDiffType(TypedDict):
    """Structured input of AwesomeVersion.diff"""

    major: bool
    minor: bool
    patch: bool
    modifier: bool
    strategy: bool
