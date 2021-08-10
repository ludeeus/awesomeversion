"""Version matchers for AwesomeVersion."""
import re

from .strategy import AwesomeVersionStrategy

RE_CALVER = re.compile(r"^(\d{2}|\d{4})\.\d{0,2}?\.?(\d{0,2}?\.?)?(\d*(\w+\d+)?)$")
RE_SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
)
RE_PEP440 = re.compile(
    r"^([1-9][0-9]*!)?(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))*((a|b|rc)"
    r"(0|[1-9][0-9]*))?(\.post(0|[1-9][0-9]*))?(\.dev(0|[1-9][0-9]*))?(\.rc(0|[1-9][0-9]*))?$"
)
RE_BUILDVER = re.compile(r"^\d+$")

RE_SPECIAL_CONTAINER = re.compile(r"^(latest|dev|stable|beta)$")

RE_SIMPLE = re.compile(r"^[v|V]?((\d+)?\.?)*$")

RE_DIGIT = re.compile(r"[a-z]*(\d+)[a-z]*")
RE_VERSION = re.compile(r"^(v|V)?(.*)$")
RE_MODIFIER = re.compile(r"^((?:\d+\-|\d|))(([a-z]+)\.?(\d*))$")


def is_buildver(version: str) -> bool:
    """Return True if the version is BuildVer."""
    return RE_BUILDVER.match(version) is not None


def is_calver(version: str) -> bool:
    """Return True if the version is CalVer."""
    return RE_CALVER.match(version) is not None


def is_semver(version: str) -> bool:
    """Return True if the version is SemVer."""
    return RE_SEMVER.match(version) is not None


def is_pep440(version: str) -> bool:
    """Return True if the version is PEP 440 compliant."""
    return RE_PEP440.match(version) is not None


def is_simple(version: str) -> bool:
    """Return True if the version is simple."""
    return RE_SIMPLE.match(version) is not None


def is_special_container(version: str) -> bool:
    """Return True if the version is specialcontainer."""
    return RE_SPECIAL_CONTAINER.match(version) is not None


def version_strategy(version: str) -> AwesomeVersionStrategy:
    """Return the version stragegy."""
    strategy = AwesomeVersionStrategy.UNKNOWN
    if is_buildver(version):
        strategy = AwesomeVersionStrategy.BUILDVER
    elif is_calver(version):
        strategy = AwesomeVersionStrategy.CALVER
    elif is_semver(version):
        strategy = AwesomeVersionStrategy.SEMVER
    elif is_special_container(version):
        strategy = AwesomeVersionStrategy.SPECIALCONTAINER
    elif is_simple(version):
        strategy = AwesomeVersionStrategy.SIMPLEVER
    elif is_pep440(version):
        strategy = AwesomeVersionStrategy.PEP440
    return strategy
