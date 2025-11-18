"""Test for trailing zeros equality in version comparison."""

# Versions like "1.0" should be considered equal to "1.0.0"
from awesomeversion import AwesomeVersion, AwesomeVersionStrategy


def test_trailing_zeros_equality() -> None:
    """Test that versions with trailing zeros are considered equal."""
    # Test the specific case from the issue
    version = AwesomeVersion("1.0", ensure_strategy=AwesomeVersionStrategy.SIMPLEVER)
    version2 = AwesomeVersion("1.0.0", ensure_strategy=AwesomeVersionStrategy.SIMPLEVER)
    assert version == version2
    assert version >= version2
    assert version <= version2
    assert not version > version2
    assert not version < version2


def test_trailing_zeros_equality_various_formats() -> None:
    """Test trailing zeros equality with various version formats."""
    test_cases = [
        ("1.0", "1.0.0"),
        ("1.0.0", "1.0"),
        ("2.1", "2.1.0.0"),
        ("1", "1.0.0"),
        ("1.0.0", "1.0.0.0"),
        ("3.2.1", "3.2.1.0"),
    ]

    for version_a, version_b in test_cases:
        ver_a = AwesomeVersion(version_a)
        ver_b = AwesomeVersion(version_b)
        assert ver_a == ver_b, f"{version_a} should equal {version_b}"
        assert ver_b == ver_a, f"{version_b} should equal {version_a}"


def test_trailing_zeros_with_different_modifiers_not_equal() -> None:
    """Test that versions with different modifiers are not equal."""
    # Even if sections match, modifiers should make them unequal
    test_cases = [
        ("1.0.0", "1.0.0-beta"),
        ("1.0", "1.0.0b0"),
        ("1.0.0-beta", "1.0.0-beta.1"),
    ]

    for version_a, version_b in test_cases:
        ver_a = AwesomeVersion(version_a)
        ver_b = AwesomeVersion(version_b)
        assert ver_a != ver_b, f"{version_a} should NOT equal {version_b}"
        assert ver_b != ver_a, f"{version_b} should NOT equal {version_a}"
