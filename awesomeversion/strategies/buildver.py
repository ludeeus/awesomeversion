"""AwesomVersion continous build versioning implementation."""
import re

from ..const import AwesomeVersionStrategy
from .base import AwesomeVersionStrategyBase


class AwesomeVersionStrategyBuildVer(AwesomeVersionStrategyBase):
    """AwesomVersion continous build versioning implementation."""

    REGEX_MATCH = re.compile(r"^\d+$")
    STRATEGY = AwesomeVersionStrategy.BUILDVER
