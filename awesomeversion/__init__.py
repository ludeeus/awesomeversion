"""Initialize the AwesomeVersion package."""
from .awesomeversion import AwesomeVersion
from .comparehandlers.base import AwesomeVersionCompareHandler
from .const import AwesomeVersionStrategy
from .exceptions import (
    AwesomeVersionCompare,
    AwesomeVersionException,
    AwesomeVersionStrategyException,
)
from .strategies.base import AwesomeVersionStrategyBase
