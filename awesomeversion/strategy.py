"""Strategies for AwesomeVersion."""
from enum import Enum


class AwesomeVersionStrategy(str, Enum):
    """Strategy enum."""

    BUILDVER = "BuildVer"
    CALVER = "CalVer"
    SEMVER = "SemVer"
    SIMPLEVER = "SimpleVer"
    UNKNOWN = "unknown"

    SPECIALCONTAINER = "SpecialContainer"
