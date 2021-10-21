"""Strategies for AwesomeVersion."""
from enum import Enum
from typing import Dict, Pattern

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


VERSION_STRATEGIES: Dict[AwesomeVersionStrategy, Pattern[str]] = {
    AwesomeVersionStrategy.BUILDVER: RE_BUILDVER,
    AwesomeVersionStrategy.CALVER: RE_CALVER,
    AwesomeVersionStrategy.SEMVER: RE_SEMVER,
    AwesomeVersionStrategy.SPECIALCONTAINER: RE_SPECIAL_CONTAINER,
    AwesomeVersionStrategy.SIMPLEVER: RE_SIMPLE,
    AwesomeVersionStrategy.PEP440: RE_PEP440,
}
