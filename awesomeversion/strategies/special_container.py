"""AwesomVersion special version implementation for containers."""
import re

from ..const import AwesomeVersionStrategy
from .base import AwesomeVersionStrategyBase


class AwesomeVersionStrategySpecialContainer(AwesomeVersionStrategyBase):
    """AwesomVersion special version implementation for containers."""

    REGEX_MATCH = re.compile(r"^(latest|dev|stable|beta)$")
    STRATEGY = AwesomeVersionStrategy.SPECIALCONTAINER
