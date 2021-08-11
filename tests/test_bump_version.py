"""test_bump_version"""
import pytest

from awesomeversion import (
    AwesomeVersion,
    AwesomeVersionNotImplementedError,
    AwesomeVersionStrategy,
)


def test_bump_version_invalid():
    """test_bump_version invalid"""
    version = AwesomeVersion("unkown")
    assert version.strategy == AwesomeVersionStrategy.UNKNOWN
    with pytest.raises(AwesomeVersionNotImplementedError):
        version.bump_version()


@pytest.mark.parametrize(
    "current, expected",
    (
        ("1", "2"),
        ("100", "101"),
        ("2021", "2022"),
    ),
)
def test_bump_version_buildver(current, expected):
    """test_bump_version BUILDVER"""
    version = AwesomeVersion(current)
    version.bump_version()
    assert version.strategy == AwesomeVersionStrategy.BUILDVER
    assert version.string == expected


@pytest.mark.parametrize(
    "current, expected, section",
    (
        ("1.2.3", "1.2.4", "patch"),
        ("1.2.3", "2.0.0", "major"),
        ("1.2.3", "1.3.0", "minor"),
    ),
)
def test_bump_version_semver(current, expected, section):
    """test_bump_version SEMVER"""
    version = AwesomeVersion(current)
    version.bump_version(**{section: True})
    assert version.strategy == AwesomeVersionStrategy.SEMVER
    assert version.string == expected
