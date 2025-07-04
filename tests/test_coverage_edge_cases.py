"""Tests for edge cases to ensure 100% code coverage."""

from __future__ import annotations

from unittest.mock import patch

from awesomeversion import AwesomeVersion, AwesomeVersionStrategy
from awesomeversion.utils.regex import get_compiled_pattern


def test_hexver_modifier_type() -> None:
    """Test that HexVer strategy returns None for modifier_type."""
    av = AwesomeVersion("0xABCD")
    assert av.strategy == AwesomeVersionStrategy.HEXVER
    assert av.modifier_type is None


def test_get_compiled_pattern_missing() -> None:
    """Test get_compiled_pattern with non-existent pattern name."""
    result = get_compiled_pattern("NON_EXISTENT_PATTERN")
    assert result is None


def test_buildver_section_valueerror() -> None:
    """Test BuildVer section method ValueError handling."""
    av = AwesomeVersion("123")
    assert av.strategy == AwesomeVersionStrategy.BUILDVER

    # Mock the string property to return something that will cause ValueError in int()
    with patch.object(
        type(av), "string", new_callable=lambda: property(lambda self: "not_a_number")
    ):
        result = av.section(0)
        assert result == 0  # Should return 0 due to ValueError
