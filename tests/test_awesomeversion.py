"""Test awesomeversion."""
import json
import warnings

import pytest

from awesomeversion import (
    AwesomeVersion,
    AwesomeVersionStrategy,
    AwesomeVersionStrategyException,
)
from awesomeversion.exceptions import AwesomeVersionException
from awesomeversion.strategy import COMPARABLE_STRATEGIES
from awesomeversion.typing import VersionType


def test_awesomeversion() -> None:
    """Test awesomeversion."""
    version = AwesomeVersion("2020.12.1")
    assert not version.beta
    assert version.valid

    version = AwesomeVersion("2020.12.1a0")
    assert version.alpha
    assert version.valid

    version = AwesomeVersion("2020.12.1b0")
    assert version.beta
    assert version.valid

    version = AwesomeVersion("2020.12.1dev0")
    assert version.dev
    assert version.valid

    version = AwesomeVersion("2020.12.1d0")
    assert version.dev
    assert version.valid

    version = AwesomeVersion("2020.12.1rc0")
    assert version.release_candidate
    assert version.prefix is None
    assert version.valid

    version = AwesomeVersion("v2020.12.1rc0")
    assert version.prefix == "v"
    assert version.valid

    version2 = AwesomeVersion(version)
    assert version == version2
    assert str(version) == str(version2)

    assert str(version) == "v2020.12.1rc0"
    assert version.string == "2020.12.1rc0"
    assert repr(version) == "<AwesomeVersion CalVer '2020.12.1rc0'>"

    assert AwesomeVersion("1.0.0-beta.2").modifier == "beta.2"
    assert AwesomeVersion("2020.2.0b1").modifier_type == "b"

    with AwesomeVersion("20.12.0") as current:
        with AwesomeVersion("20.12.1") as upstream:
            assert upstream > current


def test_major() -> None:
    """Test major."""
    assert AwesomeVersion("1.0.0.0").major == 1
    assert AwesomeVersion("1.0.0").major == 1
    assert AwesomeVersion("1.0").major == 1
    assert AwesomeVersion("1").major == 1


def test_minor() -> None:
    """Test minor."""
    assert AwesomeVersion("1.1.0.0").minor == 1
    assert AwesomeVersion("1.1.0").minor == 1
    assert AwesomeVersion("1.1").minor == 1
    assert AwesomeVersion("1").minor is None


def test_patch() -> None:
    """Test patch."""
    assert AwesomeVersion("1.1.1.1").patch == 1
    assert AwesomeVersion("1.1.1").patch == 1
    assert AwesomeVersion("1.1").patch is None
    assert AwesomeVersion("1").patch is None


def test_serialization() -> None:
    """Test to and from JSON serialization."""
    version = AwesomeVersion("20.12.1")
    dumps = json.dumps({"version": version})
    assert dumps == '{"version": "20.12.1"}'

    assert json.loads(dumps)["version"] == version.string


test_data = [
    ("2020.12.1b0"),
    ("2020.12.1"),
    ("2021.2.0.dev20210118"),
]


@pytest.mark.parametrize("version", test_data)
def test_nesting(version: VersionType) -> None:
    """Test nesting AwesomeVersion objects."""
    obj = AwesomeVersion(version)
    assert obj.string == version
    assert str(obj) == version
    assert AwesomeVersion(obj) == AwesomeVersion(version)
    assert AwesomeVersion(obj).string == AwesomeVersion(version)
    assert str(AwesomeVersion(obj)) == AwesomeVersion(version)
    assert AwesomeVersion(obj) == version
    assert AwesomeVersion(obj).string == version
    assert str(AwesomeVersion(obj)) == version

    assert (
        AwesomeVersion(
            AwesomeVersion(AwesomeVersion(AwesomeVersion(AwesomeVersion(obj))))
        )
        == version
    )

    assert (
        AwesomeVersion(
            AwesomeVersion(AwesomeVersion(AwesomeVersion(AwesomeVersion(obj))))
        ).string
        == version
    )

    assert str(
        (
            AwesomeVersion(
                AwesomeVersion(AwesomeVersion(AwesomeVersion(AwesomeVersion(obj))))
            )
        )
        == version
    )


def test_ensure_strategy() -> None:
    """test ensure_strategy."""
    obj = AwesomeVersion("1.0.0", ensure_strategy=COMPARABLE_STRATEGIES)
    assert obj.strategy == AwesomeVersionStrategy.SEMVER

    obj = AwesomeVersion(
        "1.0.0",
        [AwesomeVersionStrategy.SEMVER, AwesomeVersionStrategy.SPECIALCONTAINER],
    )
    assert obj.strategy in [
        AwesomeVersionStrategy.SEMVER,
        AwesomeVersionStrategy.SPECIALCONTAINER,
    ]

    with pytest.raises(AwesomeVersionStrategyException):
        AwesomeVersion("1", AwesomeVersionStrategy.SEMVER)

    with pytest.raises(AwesomeVersionStrategyException):
        AwesomeVersion("1", AwesomeVersionStrategy.UNKNOWN)

    with pytest.raises(AwesomeVersionStrategyException):
        AwesomeVersion(
            "1",
            [AwesomeVersionStrategy.SEMVER, AwesomeVersionStrategy.SPECIALCONTAINER],
        )


@pytest.mark.parametrize(
    "version,strategy,result",
    [
        ("14.0 (Debian 14.0-1.pgdg110+1)", AwesomeVersionStrategy.SIMPLEVER, "14.0"),
        (
            "PostgreSQL 11.13 (Debian 11.13-0+deb10u1) on x86_64-pc-linux-gnu",
            AwesomeVersionStrategy.SIMPLEVER,
            "11.13",
        ),
        (
            "5.7.26-0ubuntu0.18.04.1",
            AwesomeVersionStrategy.SIMPLEVER,
            "5.7.26",
        ),
        (
            "5.7.26-0ubuntu0.18.04.1",
            AwesomeVersionStrategy.CALVER,
            "18.04.1",
        ),
        (
            "0.4.7-MariaDB",
            AwesomeVersionStrategy.SIMPLEVER,
            "0.4.7",
        ),
        (
            "10.4.7-MariaDB-log-ubuntu0.18.04.1-whatever",
            AwesomeVersionStrategy.SIMPLEVER,
            "10.4.7",
        ),
        (
            "Linux 2b4de6616b33 5.11.0-38-generic #42~20.04.1-Ubuntu",
            AwesomeVersionStrategy.SEMVER,
            "5.11.0-38",
        ),
    ],
)
def test_find_first_match(
    version: VersionType,
    strategy: AwesomeVersionStrategy,
    result: str,
) -> None:
    """Test find_first_match"""
    obj = AwesomeVersion(
        version=version,
        ensure_strategy=strategy,
        find_first_match=True,
    )
    assert obj.string == result
    assert AwesomeVersion(version, strategy, True).string == obj.string


def test_find_first_match_exception() -> None:
    """Test"""
    with warnings.catch_warnings(record=True) as warning_list:
        assert AwesomeVersion("1", find_first_match=True)
        assert "Can not use find_first_match without ensure_strategy" in str(
            warning_list[-1].message
        )


def test_diff() -> None:
    """Test .diff"""
    version = AwesomeVersion("2020.12.1")

    assert version.diff("2021.12.1").major
    assert not version.diff("2021.12.1").minor
    assert not version.diff("2021.12.1").patch
    assert not version.diff("2021.12.1").modifier
    assert not version.diff("2021.12.1").strategy

    assert version.diff("2021.11.1").minor
    assert version.diff("2021.12.2").patch
    assert version.diff("2021.12.1dev2").modifier
    assert version.diff("2.11.1").strategy

    diff = version - "2021.12.1"
    assert diff.major
    assert diff.__repr__().startswith("AwesomeVersionDiff(")

    with pytest.raises(AwesomeVersionException):
        version.diff(None)
