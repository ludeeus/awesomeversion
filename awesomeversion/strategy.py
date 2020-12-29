"""Strategies for AwesomeVersion."""
import re
from dataclasses import dataclass
from enum import Enum

RE_SPECIAL_CONTAINER = re.compile(r"^(latest|dev|stable|beta)$")


@dataclass
class SpecialHandler:
    re: re.Pattern
    map: dict


class SpecialHandlers:
    container = SpecialHandler(
        RE_SPECIAL_CONTAINER, {"stable": 1, "beta": 2, "latest": 3, "dev": 4}
    )


class AwesomeVersionStrategy(str, Enum):
    """Strategy enum."""

    BUILDVER = "BuildVer"
    CALVER = "CalVer"
    SEMVER = "SemVer"
    SIMPLEVER = "SimpleVer"
    SPECIALCONTAINER = "SpecialContainer"
    UNKNOWN = "unknown"
