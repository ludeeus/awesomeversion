"""AwesomVersion simple versioning implementation."""
import re

from ..const import AwesomeVersionStrategy
from .base import AwesomeVersionStrategyBase

RE_SIMPLE = re.compile(r"^[v|V]?((\d+)?\.?)*$")


class AwesomeVersionStrategySimple(AwesomeVersionStrategyBase):
    """AwesomVersion simple versioning implementation."""

    REGEX_MATCH = RE_SIMPLE
    STRATEGY = AwesomeVersionStrategy.SIMPLEVER
