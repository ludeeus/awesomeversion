"""Common constants for AwesomeVersion."""
import logging
from enum import Enum
from re import Pattern
from re import compile as regex_compile

RE_DIGIT = regex_compile(r"[a-z]*(\d+)[a-z]*")
RE_MODIFIER = regex_compile(r"^((?:\d+\-|\d|))(([a-z]+)\.?(\d*))$")
RE_MODIFIER: Pattern = regex_compile(r"^((?:\d+\-|\d|))(([a-z]+)\.?(\d*))$")
RE_VERSION = regex_compile(r"^(v|V)?(.*)$")

LOGGER: logging.Logger = logging.getLogger(__package__)


class AwesomeVersionStrategy(str, Enum):
    """Strategy enum."""

    BUILDVER = "BuildVer"
    CALVER = "CalVer"
    SEMVER = "SemVer"
    SIMPLEVER = "SimpleVer"
    PEP440 = "PEP 440"
    UNKNOWN = "unknown"

    SPECIALCONTAINER = "SpecialContainer"
