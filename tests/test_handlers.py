"""Test compare handlers."""
from typing import Optional

import pytest

from awesomeversion import AwesomeVersion
from awesomeversion.comparehandlers.modifier import ComparelHandlerSemVerModifier
from awesomeversion.handlers import CompareHandlers
from awesomeversion.typing import VersionType


@pytest.mark.parametrize(
    "ver_a,ver_b,result",
    (
        (False, True, False),
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
        ("1.0.0", "stable", False),
    ),
)
def test_compare_handlers(
    ver_a: VersionType,
    ver_b: VersionType,
    result: Optional[bool],
) -> None:
    """Test handlers."""
    handler = CompareHandlers(AwesomeVersion(ver_a), AwesomeVersion(ver_b))
    assert handler.check() == result


def test_semver_modifier() -> None:
    """Test semver modifier."""
    handler = ComparelHandlerSemVerModifier(
        AwesomeVersion("1.0"), AwesomeVersion("1.0")
    )
    assert handler.handler() is None
