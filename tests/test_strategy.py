"""Test match."""
import pytest

from awesomeversion.match import version_strategy
from awesomeversion.strategy import AwesomeVersionStrategy

test_data = [
    ("123", AwesomeVersionStrategy.BUILDVER),
    ("20.1.0", AwesomeVersionStrategy.CALVER),
    ("0.118.0", AwesomeVersionStrategy.SEMVER),
    ("1.2.3.4.5", AwesomeVersionStrategy.SIMPLEVER),
    ("string", AwesomeVersionStrategy.UNKNOWN),
    ("latest", AwesomeVersionStrategy.SPECIALCONTAINER),
    ("stable", AwesomeVersionStrategy.SPECIALCONTAINER),
    ("beta", AwesomeVersionStrategy.SPECIALCONTAINER),
    ("dev", AwesomeVersionStrategy.SPECIALCONTAINER),
]


@pytest.mark.parametrize("version,strategy", test_data)
def test_strategy_match(version, strategy):
    """Test that the version matches the expected strategy."""
    assert version_strategy(version) == strategy
