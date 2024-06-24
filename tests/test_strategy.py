"""Test match."""

import pytest

from awesomeversion import AwesomeVersion
from awesomeversion.strategy import AwesomeVersionStrategy
from awesomeversion.typing import VersionType


@pytest.mark.parametrize(
    "version,strategy",
    [
        *[
            (v, AwesomeVersionStrategy.BUILDVER)
            for v in (
                "1",
                "123",
                "0",
            )
        ],
        *[
            (v, AwesomeVersionStrategy.CALVER)
            for v in (
                "20.1.0",
                "20.1",
                "2021.1.0.0",
            )
        ],
        *[
            (v, AwesomeVersionStrategy.PEP440)
            for v in (
                "1.0a1",
                "1.0.dev1",
                "1.0b2.post345.dev456",
                "1.dev0",
                "1.0.dev456",
                "1.0a1",
                "1.0a2.dev456",
                "1.0a12.dev456",
                "1.0a12",
                "1.0b1.dev456",
                "1.0b2",
                "1.0b2.post345.dev456",
                "1.0b2.post345",
                "1.0rc1.dev456",
                "1.0rc1",
                "1.0.post456.dev34",
                "1.0.post456",
                "1.1.dev1",
                "1.1-dev1",
                "1.1dev1",
                "1.1_dev1",
            )
        ],
        *[
            (v, AwesomeVersionStrategy.SEMVER)
            for v in (
                "0.118.0",
                "1.0.0-alpha",
                "1.0.0-alpha+1.2",
                "1.0.0",
                "1.2.3",
                "1.8.2-beta.1.10",
                "1.8.2-beta.1.13",
                "2.1.3",
                "2.4.6-8",
                "1.8.2-beta.1.10+somebuild",
            )
        ],
        *[
            (v, AwesomeVersionStrategy.SIMPLEVER)
            for v in (
                "1.0",
                "0.1",
                "1.2.3.4.5",
            )
        ],
        *[
            (v, AwesomeVersionStrategy.SPECIALCONTAINER)
            for v in (
                "beta",
                "dev",
                "latest",
                "stable",
            )
        ],
        *[
            (v, AwesomeVersionStrategy.UNKNOWN)
            for v in (
                "",
                "unknown",
                None,
                False,
                True,
                str,
                AwesomeVersionStrategy,
            )
        ],
    ],
)
def test_strategy_match(version: VersionType, strategy: AwesomeVersionStrategy) -> None:
    """Test that the version matches the expected strategy."""
    assert AwesomeVersion(version).strategy == strategy

    if strategy != AwesomeVersionStrategy.UNKNOWN:
        awesome_version = AwesomeVersion(
            version,
            ensure_strategy=strategy,
            find_first_match=True,
        )
        assert awesome_version.valid
        assert awesome_version.strategy == strategy
