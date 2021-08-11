"""Initialize the AwesomeVersion package."""
from .awesomeversion import AwesomeVersion
from .exceptions import (
    AwesomeVersionCompare,
    AwesomeVersionException,
    AwesomeVersionNotImplementedError,
    AwesomeVersionStrategyException,
)
from .strategy import AwesomeVersionStrategy
