"""AwesomVersion Semantic Versioning implementation."""
import re

from ..const import AwesomeVersionStrategy
from .base import AwesomeVersionStrategyBase


class AwesomeVersionStrategyCalVer(AwesomeVersionStrategyBase):
    """AwesomVersion Semantic Versioning implementation."""

    REGEX_MATCH = re.compile(
        r"^(\d{2}|\d{4})\.\d{0,2}?\.?(\d{0,2}?\.?)?(\d*(\w+\d+)?)$"
    )
    STRATEGY = AwesomeVersionStrategy.CALVER
