"""Tests for the validate util."""

import pytest

from awesomeversion.utils.validate import value_is_base16


@pytest.mark.parametrize(
    ("value", "expected"),
    (
        ("0x0", True),
        ("0xah", False),
        ("0", True),
    ),
)
def test_value_is_base16(value: str, expected: bool) -> None:
    """Test value is base16."""
    assert value_is_base16(value) == expected
