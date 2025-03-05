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


class AwesomeVersionValueCache(TypedDict):
    """TypedDict for AwesomeVersion value cache."""

    major: AwesomeVersion | None | object
    minor: AwesomeVersion | None | object
    patch: AwesomeVersion | None | object
    prefix: str | None | object
