"""Strategies for AwesomeVersion."""
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Pattern, Tuple

from .utils.regex import (
    RE_BUILDVER,
    RE_CALVER,
    RE_PEP440,
    RE_SEMVER,
    RE_SIMPLE,
    RE_SPECIAL_CONTAINER,
)


class AwesomeVersionStrategy(str, Enum):
    """Strategy enum."""

    BUILDVER = "BuildVer"
    CALVER = "CalVer"
    SEMVER = "SemVer"
    SIMPLEVER = "SimpleVer"
    PEP440 = "PEP 440"
    UNKNOWN = "unknown"

    SPECIALCONTAINER = "SpecialContainer"


@dataclass
class AwesomeVersionStrategyDescription:
    """Description of a strategy."""

    strategy: AwesomeVersionStrategy
    pattern: Pattern[str]


VERSION_STRATEGIES: Tuple[AwesomeVersionStrategyDescription, ...] = (
    AwesomeVersionStrategyDescription(
        strategy=AwesomeVersionStrategy.BUILDVER,
        pattern=RE_BUILDVER,
    ),
    AwesomeVersionStrategyDescription(
        strategy=AwesomeVersionStrategy.CALVER,
        pattern=RE_CALVER,
    ),
    AwesomeVersionStrategyDescription(
        strategy=AwesomeVersionStrategy.SEMVER,
        pattern=RE_SEMVER,
    ),
    AwesomeVersionStrategyDescription(
        strategy=AwesomeVersionStrategy.SPECIALCONTAINER,
        pattern=RE_SPECIAL_CONTAINER,
    ),
    AwesomeVersionStrategyDescription(
        strategy=AwesomeVersionStrategy.SIMPLEVER,
        pattern=RE_SIMPLE,
    ),
    AwesomeVersionStrategyDescription(
        strategy=AwesomeVersionStrategy.PEP440,
        pattern=RE_PEP440,
    ),
)


VERSION_STRATEGIES_DICT: Dict[
    AwesomeVersionStrategy, AwesomeVersionStrategyDescription
] = {description.strategy: description for description in VERSION_STRATEGIES}
