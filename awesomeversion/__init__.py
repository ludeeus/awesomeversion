"""Initialize the AwesomeVersion package."""
from .awesomeversion import AwesomeVersion
from .exceptions import (
    AwesomeVersionCompareException,
    AwesomeVersionException,
    AwesomeVersionStrategyException,
)
from .strategy import COMPARABLE_STRATEGIES, AwesomeVersionStrategy

__all__ = [
    "AwesomeVersion",
    "AwesomeVersionCompareException",
    "AwesomeVersionException",
    "AwesomeVersionStrategy",
    "AwesomeVersionStrategyException",
    "COMPARABLE_STRATEGIES",
]
