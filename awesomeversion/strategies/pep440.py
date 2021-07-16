"""AwesomVersion PEP440 versioning implementation."""
import re

from ..const import AwesomeVersionStrategy
from .base import AwesomeVersionStrategyBase


class AwesomeVersionStrategyPep440(AwesomeVersionStrategyBase):
    """AwesomVersion PEP440 versioning implementation."""

    REGEX_MATCH = re.compile(
        r"^([1-9][0-9]*!)?(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))*((a|b|rc)(0|[1-9][0-9]*))?(\.post(0|[1-9][0-9]*))?(\.dev(0|[1-9][0-9]*))?(\.rc(0|[1-9][0-9]*))?$"
    )
    STRATEGY = AwesomeVersionStrategy.PEP440
