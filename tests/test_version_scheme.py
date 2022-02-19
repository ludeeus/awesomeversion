"""Test test_version_scheme."""
import pytest

from awesomeversion import AwesomeVersion
from awesomeversion.strategy import AwesomeVersionStrategy
from awesomeversion.typing import VersionType


@pytest.mark.parametrize(
    "version,strategy,dev,beta,modifier_type",
    [
        ("0.118.0", AwesomeVersionStrategy.SEMVER, False, False, None),
        ("1.0.0b1", AwesomeVersionStrategy.PEP440, False, True, "b"),
        ("1.0.0-beta.1", AwesomeVersionStrategy.SEMVER, False, True, "beta"),
        ("v1.0.0-beta.1", AwesomeVersionStrategy.SEMVER, False, True, "beta"),
        ("2021.2.0.dev1", AwesomeVersionStrategy.CALVER, True, False, "dev"),
        ("stable", AwesomeVersionStrategy.SPECIALCONTAINER, False, False, None),
    ],
)
def test_version_scheme(
    version: VersionType,
    strategy: AwesomeVersionStrategy,
    dev: bool,
    beta: bool,
    modifier_type: str | None,
) -> None:
    """Test that the version matches the expected scheme."""
    version_object = AwesomeVersion(version)
    assert str(version_object) == version
    assert version_object.strategy == strategy
    assert version_object.dev == dev
    assert version_object.beta == beta
    assert version_object.modifier_type == modifier_type


def test_semver_sections() -> None:
    """Test semver sections."""
    ver_a = AwesomeVersion("1.0.0-beta.1")
    ver_b = AwesomeVersion("2.0.0")
    assert ver_a.strategy == AwesomeVersionStrategy.SEMVER
    assert ver_b.strategy == AwesomeVersionStrategy.SEMVER

    assert ver_a.major == "1"
    assert ver_a.minor == "0"
    assert ver_a.patch == "0"

    assert ver_a.major < ver_b.major


def test_semver_sections_for_non_semver() -> None:
    """Test semver sections for non semver versions."""
    version = AwesomeVersion("2020.01.1")
    assert version.major is None
    assert version.minor is None
    assert version.patch is None
