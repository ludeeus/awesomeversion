"""Strategies for AwesomeVersion."""
from enum import Enum

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


VERSION_STRATEGIES = (
    (RE_BUILDVER, AwesomeVersionStrategy.BUILDVER),
    (RE_CALVER, AwesomeVersionStrategy.CALVER),
    (RE_SEMVER, AwesomeVersionStrategy.SEMVER),
    (RE_SPECIAL_CONTAINER, AwesomeVersionStrategy.SPECIALCONTAINER),
    (RE_SIMPLE, AwesomeVersionStrategy.SIMPLEVER),
    (RE_PEP440, AwesomeVersionStrategy.PEP440),
)
