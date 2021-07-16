"""Test custom."""
import re
import pytest
from awesomeversion import (
    AwesomeVersion,
    AwesomeVersionStrategyBase,
    AwesomeVersionStrategyException,
)


class AwesomeVersionStrategyTest(AwesomeVersionStrategyBase):
    """Custom Version Strategy."""

    REGEX_MATCH = re.compile(r"test")
    STRATEGY = "TestVer"


def test_custom():
    version_a = AwesomeVersion("test", custom_strategies=[AwesomeVersionStrategyTest])
    assert version_a.strategy == "TestVer"
    assert repr(version_a) == "<AwesomeVersion TestVer 'test'>"

    version_b = AwesomeVersion(
        "not_test", custom_strategies=[AwesomeVersionStrategyTest]
    )
    assert version_b.strategy != "TestVer"
    assert repr(version_b) == "<AwesomeVersion unknown 'not_test'>"


def test_invalid():
    AwesomeVersion("test", custom_strategies=["Invalid"])
    with pytest.raises(AwesomeVersionStrategyException):
        AwesomeVersion("test", custom_strategies=["Invalid"])
