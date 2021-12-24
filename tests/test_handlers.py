"""Test compare handlers."""
from typing import Optional

import pytest

from awesomeversion import AwesomeVersion
from awesomeversion.comparehandlers.modifier import compare_handler_semver_modifier
from awesomeversion.typing import VersionType


@pytest.mark.parametrize(
    "ver_a,ver_b,result",
    (
        (False, True, None),
        ("2", "1", True),
        ("1", "2", False),
        ("1", "1", False),
        ("1.0", "1.0", False),
        ("5.10", "5.10", False),
        ("1.2.3.4.5b0", "1.2b0", True),
        ("1.0b1", "1.0b0", True),
        ("1.0", "1.0b0", True),
        ("1.0b0", "1.0b1", False),
        ("1.0b0", "1.0", False),
        ("1.dev1", "1.dev0", True),
        ("1.dev0", "1.dev1", False),
        ("latest", "stable", True),
        ("latest", "1", True),
        ("1.2.3.4.5.6.7.8.9", "1.2.3.4.5.6.7.8.9", False),
        ("1.0.0", "stable", False),
    ),
)
def test_compare_handlers(
    ver_a: VersionType,
    ver_b: VersionType,
    result: Optional[bool],
) -> None:
    """Test handlers."""
    version_a = AwesomeVersion(ver_a)
    version_b = AwesomeVersion(ver_b)

    if (
        version_a.strategy_description is not None
        or version_b.strategy_description is not None
    ):
        assert (AwesomeVersion(ver_a) > ver_b) == result


def test_semver_modifier() -> None:
    """Test semver modifier."""
    result = compare_handler_semver_modifier(
        AwesomeVersion("1.0"), AwesomeVersion("1.0")
    )
    assert result is None
