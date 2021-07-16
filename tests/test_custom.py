"""Test custom."""
import re

import pytest

from awesomeversion import (
    AwesomeVersion,
    AwesomeVersionCompareHandler,
    AwesomeVersionException,
    AwesomeVersionStrategyBase,
)


class AwesomeVersionStrategyTest(AwesomeVersionStrategyBase):
    """Custom Version Strategy."""

    REGEX_MATCH = re.compile(r"test")
    STRATEGY = "TestVer"


class AwesomeVersionStrategyInvalid(AwesomeVersionStrategyBase):
    """Custom Version Strategy."""


class AwesomeVersionCompareHandlerTestInvalid(AwesomeVersionCompareHandler):
    """Custom Compare Handler."""


class AwesomeVersionCompareHandlerTest(AwesomeVersionCompareHandler):
    """Custom Compare Handler."""

    def handler(self) -> bool:
        """Compare handler."""
        if self.version_a == "1.2.3":
            return True


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
    with pytest.raises(AwesomeVersionException):
        assert AwesomeVersion("test", custom_strategies=["Invalid"]).strategy

    with pytest.raises(AwesomeVersionException):
        assert AwesomeVersion(1, custom_compare_handlers=["Invalid"]) > 2

    with pytest.raises(NotImplementedError):
        assert AwesomeVersion(
            "test", custom_strategies=[AwesomeVersionStrategyInvalid]
        ).strategy

    with pytest.raises(NotImplementedError):
        assert AwesomeVersion(
            "test",
            custom_strategies=[AwesomeVersionStrategyTest],
            custom_compare_handlers=[AwesomeVersionCompareHandlerTestInvalid],
        ) > AwesomeVersion(
            "test",
            custom_strategies=[AwesomeVersionStrategyTest],
            custom_compare_handlers=[AwesomeVersionCompareHandlerTestInvalid],
        )
