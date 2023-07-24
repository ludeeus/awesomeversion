"""Test for issue #96."""
# https://github.com/ludeeus/awesomeversion/issues/96
import re

import pytest

from awesomeversion import (
    AwesomeVersion,
    AwesomeVersionStrategy,
    AwesomeVersionStrategyException,
)


def test() -> None:
    """Test for issue #96."""
    version = AwesomeVersion("10.3.0", AwesomeVersionStrategy.SEMVER)
    assert version.strategy == AwesomeVersionStrategy.SEMVER

    version = AwesomeVersion(
        "10.3.0",
        [
            AwesomeVersionStrategy.CALVER,
            AwesomeVersionStrategy.SEMVER,
            AwesomeVersionStrategy.SIMPLEVER,
            AwesomeVersionStrategy.BUILDVER,
            AwesomeVersionStrategy.PEP440,
        ],
    )
    assert version.strategy == AwesomeVersionStrategy.CALVER

    version = AwesomeVersion(
        "10.3.0",
        [
            AwesomeVersionStrategy.SEMVER,
            AwesomeVersionStrategy.CALVER,
        ],
    )
    assert version.strategy == AwesomeVersionStrategy.SEMVER

    with pytest.raises(
        AwesomeVersionStrategyException,
        match=re.escape(
            "Strategy unknown does not match ['SemVer', 'CalVer'] for whatever"
        ),
    ):
        AwesomeVersion(
            "whatever",
            [
                AwesomeVersionStrategy.SEMVER,
                AwesomeVersionStrategy.CALVER,
            ],
        )

    with pytest.raises(
        AwesomeVersionStrategyException,
        match=re.escape("Strategy CalVer does not match ['SemVer'] for 2021.12"),
    ):
        AwesomeVersion("2021.12", ensure_strategy=AwesomeVersionStrategy.SEMVER)
