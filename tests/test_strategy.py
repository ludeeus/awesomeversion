"""Test match."""
import pytest

from awesomeversion import AwesomeVersion
from awesomeversion.strategy import AwesomeVersionStrategy
from awesomeversion.typing import VersionType

BUILDVER = (
    "1",
    "123",
)
CALVER = (
    "20.1.0",
    "20.1",
)
PEP440 = (
    "1.0a1",
    "1.0.dev1",
    "1.0b2.post345.dev456",
)
SEMVER = (
    "0.118.0",
    "1.2.3",
)
SIMPLEVER = (
    "1.0",
    "1.2.3.4.5",
)
SPECIALCONTAINER = (
    "beta",
    "dev",
    "latest",
    "stable",
)
UNKNOWN = (
    "",
    "unknown",
    None,
)


@pytest.mark.parametrize(
    "version,strategy",
    [
        *[(v, AwesomeVersionStrategy.BUILDVER) for v in BUILDVER],
        *[(v, AwesomeVersionStrategy.CALVER) for v in CALVER],
        *[(v, AwesomeVersionStrategy.PEP440) for v in PEP440],
        *[(v, AwesomeVersionStrategy.SEMVER) for v in SEMVER],
        *[(v, AwesomeVersionStrategy.SIMPLEVER) for v in SIMPLEVER],
        *[(v, AwesomeVersionStrategy.SPECIALCONTAINER) for v in SPECIALCONTAINER],
        *[(v, AwesomeVersionStrategy.UNKNOWN) for v in UNKNOWN],
    ],
)
def test_strategy_match(version: VersionType, strategy: AwesomeVersionStrategy) -> None:
    """Test that the version matches the expected strategy."""
    assert AwesomeVersion(version).strategy == strategy
