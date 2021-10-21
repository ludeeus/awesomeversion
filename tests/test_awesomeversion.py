"""Test awesomeversion."""
import json

import pytest

from awesomeversion import (
    AwesomeVersion,
    AwesomeVersionStrategy,
    AwesomeVersionStrategyException,
)
from awesomeversion.typing import VersionType


def test_awesomeversion() -> None:
    """Test awesomeversion."""
    version = AwesomeVersion("2020.12.1")
    assert not version.beta

    version = AwesomeVersion("2020.12.1a0")
    assert version.alpha

    version = AwesomeVersion("2020.12.1b0")
    assert version.beta

    version = AwesomeVersion("2020.12.1dev0")
    assert version.dev

    version = AwesomeVersion("2020.12.1d0")
    assert version.dev

    version = AwesomeVersion("2020.12.1rc0")
    assert version.release_candidate
    assert version.prefix is None

    version = AwesomeVersion("v2020.12.1rc0")
    assert version.prefix == "v"

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


def test_ensure_strategy(caplog: pytest.LogCaptureFixture) -> None:
    """test ensure_strategy."""
    obj = AwesomeVersion("1.0.0", ensure_strategy=AwesomeVersionStrategy.SEMVER)
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
        AwesomeVersion(
            "1",
            [AwesomeVersionStrategy.SEMVER, AwesomeVersionStrategy.SPECIALCONTAINER],
        )

    obj = AwesomeVersion.ensure_strategy("1.0.0", AwesomeVersionStrategy.SEMVER)
    assert (
        "Using AwesomeVersion.ensure_strategy(version, strategy) is deprecated"
        in caplog.text
    )
