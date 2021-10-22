"""Test match."""
import pytest

from awesomeversion import AwesomeVersion
from awesomeversion.strategy import AwesomeVersionStrategy
from awesomeversion.typing import VersionType


@pytest.mark.parametrize(
    "version,strategy",
    [
        ("0.118.0", AwesomeVersionStrategy.SEMVER),
        ("1.2.3.4.5", AwesomeVersionStrategy.SIMPLEVER),
        ("1.0", AwesomeVersionStrategy.SIMPLEVER),
        ("v1.0", AwesomeVersionStrategy.SIMPLEVER),
        ("123", AwesomeVersionStrategy.BUILDVER),
        ("20.1.0", AwesomeVersionStrategy.CALVER),
        ("beta", AwesomeVersionStrategy.SPECIALCONTAINER),
        ("dev", AwesomeVersionStrategy.SPECIALCONTAINER),
        ("latest", AwesomeVersionStrategy.SPECIALCONTAINER),
        ("stable", AwesomeVersionStrategy.SPECIALCONTAINER),
        ("", AwesomeVersionStrategy.UNKNOWN),
        ("unknown", AwesomeVersionStrategy.UNKNOWN),
        (None, AwesomeVersionStrategy.UNKNOWN),
    ],
)
def test_strategy_match(version: VersionType, strategy: AwesomeVersionStrategy) -> None:
    """Test that the version matches the expected strategy."""
    assert AwesomeVersion(version).strategy == strategy
