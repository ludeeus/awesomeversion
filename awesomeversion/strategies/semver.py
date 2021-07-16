"""AwesomVersion Semantic Versioning implementation."""
import re

from ..const import AwesomeVersionStrategy
from .base import AwesomeVersionStrategyBase

RE_SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
)


class AwesomeVersionStrategySemVer(AwesomeVersionStrategyBase):
    """AwesomVersion Semantic Versioning implementation."""

    REGEX_MATCH = RE_SEMVER
    STRATEGY = AwesomeVersionStrategy.SEMVER
