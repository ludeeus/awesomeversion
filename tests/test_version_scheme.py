"""Test test_version_scheme."""
import pytest

from awesomeversion import AwesomeVersion, AwesomeVersionStrategy


@pytest.mark.parametrize(
    "version,strategy,dev,beta,modifier,modifier_type",
    [
        ("0.118.0", AwesomeVersionStrategy.SEMVER, False, False, None, None),
        ("1.0.0b1", AwesomeVersionStrategy.PEP440, False, True, "b1", "b"),
        ("1.0.0-beta.1", AwesomeVersionStrategy.SEMVER, False, True, "beta.1", "beta"),
        ("v1.0.0-beta.1", AwesomeVersionStrategy.SEMVER, False, True, "beta.1", "beta"),
        ("2021.2.0.dev1", AwesomeVersionStrategy.CALVER, True, False, "dev1", "dev"),
        ("stable", AwesomeVersionStrategy.SPECIALCONTAINER, False, False, None, None),
    ],
)
def test_version_scheme(version, strategy, dev, beta, modifier, modifier_type):
    """Test that the version matches the expected scheme."""
    version_object = AwesomeVersion(version)
    assert str(version_object) == version
    assert version_object.strategy == strategy
    assert version_object.dev == dev
    assert version_object.beta == beta
    assert version_object.modifier == modifier
    assert version_object.modifier_type == modifier_type


def test_semver_sections():
    """Test semver sections."""
    version_a = AwesomeVersion("1.0.0-beta.1")
    version_b = AwesomeVersion("2.0.0")
    assert version_a.strategy == AwesomeVersionStrategy.SEMVER
    assert version_b.strategy == AwesomeVersionStrategy.SEMVER

    assert version_a.major == "1"
    assert version_a.minor == "0"
    assert version_a.patch == "0"

    assert version_a.major < version_b.major


def test_semver_sections_for_non_semver():
    """Test semver sections for non semver versions."""
    version = AwesomeVersion("2020.01.1")
    assert version.major is None
    assert version.minor is None
    assert version.patch is None
