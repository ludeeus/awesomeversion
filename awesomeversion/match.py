"""Version matchers for AwesomeVersion."""
import re

from .strategy import AwesomeVersionStrategy

RE_CALVER = re.compile(r"^(\d{2}|\d{4})\.\d{0,2}?\.?(\d*(\w+\d+)?)$")
RE_SEMVER = re.compile(r"^(\d+)?\.?(\d+)?\.?(\d*(\w+\d+)?)$")
RE_BUILDVER = re.compile(r"^\d*$")

RE_SIMPLE = re.compile(r"^[v|V]?((\d+)?\.?)*$")

RE_DIGIT = re.compile(r"[a-z]*(\d+)[a-z]*")
RE_VERSION = re.compile(r"^[v|V]?(.*)$")
RE_MODIFIER = re.compile(r"^\d+(\w+\d+)?$")


def is_buildver(version: str) -> bool:
    """Return True if the version is BuildVer."""
    return RE_BUILDVER.match(version)


def is_calver(version: str) -> bool:
    """Return True if the version is CalVer."""
    return RE_CALVER.match(version)


def is_semver(version: str) -> bool:
    """Return True if the version is SemVer."""
    return RE_SEMVER.match(version)


def is_simple(version: str) -> bool:
    """Return True if the version is simple."""
    return RE_SIMPLE.match(version)


def version_strategy(version: str) -> AwesomeVersionStrategy:
    """Return the version stragegy."""
    if is_buildver(version):
        return AwesomeVersionStrategy.BUILDVER
    if is_calver(version):
        return AwesomeVersionStrategy.CALVER
    if is_semver(version):
        return AwesomeVersionStrategy.SEMVER
    if is_simple(version):
        return AwesomeVersionStrategy.SIMPLEVER
    return AwesomeVersionStrategy.UNKNOWN
