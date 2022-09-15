""""Custom types for AwesomeVersion."""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, List, Tuple, Union

from .strategy import AwesomeVersionStrategy

if TYPE_CHECKING:
    from .awesomeversion import AwesomeVersion

VersionType = Union[str, float, int, object, "AwesomeVersion"]
EnsureStrategyIterableType = Union[
    List[AwesomeVersionStrategy], Tuple[AwesomeVersionStrategy, ...]
]


EnsureStrategyType = Union[AwesomeVersionStrategy, EnsureStrategyIterableType, None]


@dataclass
class AwesomeVersionDiff:
    """Structured output of AwesomeVersion.diff"""

    major: bool
    minor: bool
    patch: bool
    modifier: bool
    strategy: bool
